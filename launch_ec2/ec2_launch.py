import random
import urllib
import ssl
import certifi
import urllib3
from botocore.exceptions import ClientError


def create_key_pair(key_name, aws_ec2_client):
    try:
        response = aws_ec2_client.create_key_pair(KeyName=key_name,
                                                  KeyType="rsa",
                                                  KeyFormat="pem")
        key_id = response.get("KeyPairId")
        with open(f"{key_name}.pem", "w") as file:
            file.write(response.get("KeyMaterial"))
        print("Key pair id - ", key_id)
        return key_id
    except ClientError:
        print("key already exists")


def create_security_group(aws_ec2_client, name, description, VPC_ID):
    name_addition = ""
    try:
        response = aws_ec2_client.create_security_group(Description=description,
                                                        GroupName=name,
                                                        VpcId=VPC_ID)
        group_id = response.get("GroupId")

        print("Security Group Id - ", group_id)

        return group_id
    except ClientError:
        try:
            name_addition = str(random.randint(0, 999))
            name = name + name_addition
            response = aws_ec2_client.create_security_group(Description=description,
                                                            GroupName=name,
                                                            VpcId=VPC_ID)
            group_id = response.get("GroupId")

            print("Security Group Id - ", group_id)

            return group_id
        except ClientError:
            name_addition = str(random.randint(0, 999))
            name = name + name_addition
            response = aws_ec2_client.create_security_group(Description=description,
                                                            GroupName=name,
                                                            VpcId=VPC_ID)
            group_id = response.get("GroupId")

            print("Security Group Id - ", group_id)
            return group_id


def get_my_public_ip():
    external_ip = urllib.request.urlopen("https://ident.me", cafile=certifi.where()).read().decode(
        "utf8")
    print("Public ip - ", external_ip)

    return external_ip


def add_ssh_access_sg(sg_id, ip_address, aws_ec2_client):
    ip_address = f"{ip_address}/32"

    response = aws_ec2_client.authorize_security_group_ingress(
        CidrIp=ip_address,
        FromPort=22,
        GroupId=sg_id,
        IpProtocol='tcp',
        ToPort=22,
    )
    if response.get("Return"):
        print("ssh access rule added successfully")
    else:
        print("Rule was not added")


def add_http_access_sg(sg_id, aws_ec2_client):
    response = aws_ec2_client.authorize_security_group_ingress(
        CidrIp="0.0.0.0/0",
        FromPort=80,
        GroupId=sg_id,
        IpProtocol='tcp',
        ToPort=80,
    )
    if response.get("Return"):
        print("http access rule added successfully")
    else:
        print("Rule was not added")


def run_ec2(aws_ec2_client, sg_id, subnet_id, instance_name):
    response = aws_ec2_client.run_instances(
        BlockDeviceMappings=[
            {
                "DeviceName": "/dev/sda1",
                "Ebs": {
                    "DeleteOnTermination": True,
                    "VolumeSize": 10,
                    # don't have access to gp1
                    "VolumeType": "gp2",
                    "Encrypted": False
                },
            },
        ],
        # ubuntu AMI - ami-053b0d53c279acc90
        ImageId="ami-053b0d53c279acc90",
        InstanceType="t2.micro",
        KeyName="my-demo-key",
        MaxCount=1,
        MinCount=1,
        Monitoring={"Enabled": True},
        # SecurityGroupIds=[
        #     sg_id,
        # ],
        # SubnetId=subnet_id,
        UserData="""#!/bin/bash
echo "Hello I am from user data" > info.txt
""",
        InstanceInitiatedShutdownBehavior="stop",
        NetworkInterfaces=[
            {
                "AssociatePublicIpAddress": True,
                "DeleteOnTermination": True,
                "Groups": [
                    sg_id,
                ],
                "DeviceIndex": 0,
                "SubnetId": subnet_id,
            },
        ],
    )

    for instance in response.get("Instances"):
        instance_id = instance.get("InstanceId")
        print("InstanceId - ", instance_id)
    # pprint(response)

    # Create a name tag for the instance
    tag = {'Key': 'Name', 'Value': instance_name}

    # Assign the name tag to the instance
    aws_ec2_client.create_tags(Resources=[instance_id], Tags=[tag])

    return None


def stop_ec2(aws_ec2_client, instance_id):
    response = aws_ec2_client.stop_instances(InstanceIds=[
        instance_id,
    ], )
    for instance in response.get("StoppingInstances"):
        print("Stopping instance - ", instance.get("InstanceId"))


def start_ec2(aws_ec2_client, instance_id):
    response = aws_ec2_client.start_instances(InstanceIds=[
        instance_id,
    ], )
    for instance in response.get("StartingInstances"):
        print("Starting instance - ", instance.get("InstanceId"))


def terminate_ec2(aws_ec2_client, instance_id):
    response = aws_ec2_client.terminate_instances(InstanceIds=[
        instance_id,
    ], )
    for instance in response.get("TerminatingInstances"):
        print("Terminating instance - ", instance.get("InstanceId"))


def create_ec2(ec2_client, args):
    # chmod 400 my-demo-key.pem
    create_key_pair("my-demo-key", ec2_client)

    #  # VPC AND SECURITY_GROUP
    vpc_id = args.vpc_id
    subnet_id = args.subnet_id
    # vpc_id = "vpc-04ea3928999702acc"
    # subnet_id = "subnet-0c3792077ac1e7a11"
    my_ip = get_my_public_ip()
    security_group_id = create_security_group(ec2_client,
                                              "ec2-sg", "Security group to enable access on ec2", vpc_id)

    # only concrete ip rule
    add_ssh_access_sg(security_group_id, my_ip, ec2_client)
    add_http_access_sg(security_group_id, ec2_client)

    #  # EC2
    run_ec2(ec2_client, security_group_id, subnet_id, 'btu-custom-instance')

    # stop_ec2('i-0494e0d49bf8a5b43')
    # start_ec2('i-0494e0d49bf8a5b43')
    # terminate_ec2("i-0d291c92367b5ca33")


def create_bastion_host(ec2_client, args):
    vpc_id = args.vpc_id
    subnet_id = args.subnet_id
    ip_address_for_ssh = "0.0.0.0"
    security_group_id = create_security_group(ec2_client, "bastion-sg", "Security group to enable access on ec2",
                                              vpc_id)
    add_ssh_access_sg(security_group_id, ip_address_for_ssh, ec2_client)
    run_ec2(ec2_client, security_group_id, subnet_id, 'bastion_host')


def give_access_to_ssh_sg(ec2_client, sg_id):
    my_ip = get_my_public_ip()
    add_ssh_access_sg(sg_id, my_ip, ec2_client)
    print("done")
