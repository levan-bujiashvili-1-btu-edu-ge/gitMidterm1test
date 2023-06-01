import time
from pprint import pprint

from auth.auth_ec2 import init_ec2_client


def create_vpc(ec2_client):
    result = ec2_client.create_vpc(CidrBlock="10.0.0.0/16")
    my_vpc = result.get("Vpc")
    print(my_vpc)
    return my_vpc.get("VpcId")


def add_name_tag(vpc_id, ec2_client):
    ec2_client.create_tags(Resources=[vpc_id],
                           Tags=[{
                               "Key": "Name",
                               "Value": "btuVPC"
                           }])


def create_igw(ec2_client):
    result = ec2_client.create_internet_gateway()
    return result.get("InternetGateway").get("InternetGatewayId")


def attach_igw_to_vpc(vpc_id, igw_id, ec2_client):
    ec2_client.attach_internet_gateway(InternetGatewayId=igw_id, VpcId=vpc_id)


def create_subnet(vpc_id, cidr_block, subnet_name, ec2_client):
    response = ec2_client.create_subnet(VpcId=vpc_id, CidrBlock=cidr_block)
    time.sleep(2)
    subnet = response.get("Subnet")
    pprint(subnet)
    subnet_id = subnet.get("SubnetId")
    ec2_client.create_tags(
        Resources=[subnet_id],
        Tags=[
            {
                "Key": "Name",
                "Value": subnet_name
            },
        ],
    )
    return subnet_id


def create_or_get_igw(vpc_id, ec2_client):
    igw_id = None
    igw_response = ec2_client.describe_internet_gateways(
        Filters=[{
            'Name': 'attachment.vpc-id',
            'Values': [vpc_id]
        }])

    if 'InternetGateways' in igw_response and igw_response['InternetGateways']:
        igw = igw_response['InternetGateways'][0]
        igw_id = igw['InternetGatewayId']
    else:
        response = ec2_client.create_internet_gateway()
        pprint(response)
        igw = response.get("InternetGateway")
        igw_id = igw.get("InternetGatewayId")
        response = ec2_client.attach_internet_gateway(InternetGatewayId=igw_id,
                                                      VpcId=vpc_id)
        print("attached")
        pprint(response)
    return igw_id


def create_route_table_with_route(vpc_id, route_table_name, igw_id, ec2_client):
    response = ec2_client.create_route_table(VpcId=vpc_id)
    route_table = response.get("RouteTable")
    pprint(route_table)
    route_table_id = route_table.get("RouteTableId")
    print("Route table id", route_table_id)
    ec2_client.create_tags(
        Resources=[route_table_id],
        Tags=[
            {
                "Key": "Name",
                "Value": route_table_name
            },
        ],
    )
    response = ec2_client.create_route(
        DestinationCidrBlock='0.0.0.0/0',
        GatewayId=igw_id,
        RouteTableId=route_table_id,
    )
    return route_table_id


def associate_route_table_to_subnet(route_table_id, subnet_id, ec2_client):
    response = ec2_client.associate_route_table(RouteTableId=route_table_id,
                                                SubnetId=subnet_id)
    print("Route table associated")
    pprint(response)


def enable_auto_public_ips(subnet_id, action, ec2_client):
    new_state = True if action == "enable" else False
    response = ec2_client.modify_subnet_attribute(
        MapPublicIpOnLaunch={"Value": new_state}, SubnetId=subnet_id)
    print("Public IP association state changed to", new_state)


def create_route_table_without_route(vpc_id, ec2_client):
    response = ec2_client.create_route_table(VpcId=vpc_id)
    route_table = response.get("RouteTable")
    pprint(route_table)
    route_table_id = route_table.get("RouteTableId")
    print("Route table id", route_table_id)
    ec2_client.create_tags(
        Resources=[route_table_id],
        Tags=[
            {
                "Key": "Name",
                "Value": "private-route-table"
            },
        ],
    )
    return route_table_id


def setupVPC(args):
    ec2_client = init_ec2_client()
    vpc_id = create_vpc(ec2_client)
    time.sleep(5)
    add_name_tag(vpc_id, ec2_client)

    number_of_privates = args.private_subnets

    number_of_publics = number_of_privates + args.public_subnets
    number_used = []
    number_of_public_subs = []

    if args.private_subnets + args.public_subnets > 200:
        print("too many subnets")
    else:
        if args.create_vpc == "True":
            vpc_id = create_vpc(ec2_client)
            add_name_tag(vpc_id, ec2_client)
            if args.igw == "True":
                my_igw = create_igw(ec2_client)
                attach_igw_to_vpc(vpc_id, my_igw, ec2_client)

                for i in range(number_of_privates):
                    subnet_id = create_subnet(vpc_id, f'10.0.{i}.0/24', f'private_sub_{i}', ec2_client)
                    rtb_id = create_route_table_without_route(vpc_id, ec2_client)
                    associate_route_table_to_subnet(rtb_id, subnet_id, ec2_client)
                    number_used.append(i)
                    print("privates")
                    print(number_used)
                    time.sleep(3)

                for i in range(number_of_privates, number_of_publics):
                    subnet_id = create_subnet(vpc_id, f'10.0.{i}.0/24', f'public_sub_{i}', ec2_client)
                    rtb_id = create_route_table_with_route(vpc_id, 'my_route_name',
                                                           create_or_get_igw(vpc_id, ec2_client), ec2_client)
                    associate_route_table_to_subnet(rtb_id, subnet_id, ec2_client)
                    enable_auto_public_ips(subnet_id, 'enable', ec2_client)
                    number_of_public_subs.append(i)
                    print("publics")
                    print(number_of_public_subs)
                    time.sleep(3)
