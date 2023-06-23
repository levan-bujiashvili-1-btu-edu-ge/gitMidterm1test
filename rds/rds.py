import botocore
from botocore.exceptions import ClientError

from launch_ec2.ec2_launch import create_security_group

BASE_MYSQL_STORAGE = 60


def create_mysql_instance(rds_client, security_group_id, rds_identifier):
    """Creates a new RDS instance that is associated with the given security group."""
    response = rds_client.create_db_instance(
        DBName='myrds',
        DBInstanceIdentifier=rds_identifier,
        AllocatedStorage=BASE_MYSQL_STORAGE,
        DBInstanceClass='db.t4g.micro',
        Engine='mysql',
        MasterUsername='mysqlusername',
        MasterUserPassword='mysqlpass',
        VpcSecurityGroupIds=[security_group_id],
        DBSubnetGroupName="subnets_for_db",
        BackupRetentionPeriod=7,
        # port for mysql 3306
        Port=3306,
        MultiAZ=False,
        EngineVersion='8.0.32',
        AutoMinorVersionUpgrade=True,
        # Iops=123, # Necessary when StorageType is 'io1'
        PubliclyAccessible=True,
        Tags=[
            {
                'Key': 'Name',
                'Value': 'First RDS'
            },
        ],
        MaxAllocatedStorage=100,
        StorageType='gp2',
        # AllowMajorVersionUpgrade=True,
        # EnablePerformanceInsights=True, # performance insights not used with mysql
        # PerformanceInsightsRetentionPeriod=7,
        DeletionProtection=False,
    )

    _id = response.get("DBInstance").get("DBInstanceIdentifier")
    print(f"Instance {_id} was created")

    return response


def create_mysql_instance_for_bastion(rds_client, security_group_id, rds_identifier):
    """Creates a new RDS instance that is associated with the given security group."""
    response = rds_client.create_db_instance(
        DBName='myrds',
        DBInstanceIdentifier=rds_identifier,
        AllocatedStorage=BASE_MYSQL_STORAGE,
        DBInstanceClass='db.t4g.micro',
        Engine='mysql',
        MasterUsername='mysqlusername',
        MasterUserPassword='mysqlpass',
        VpcSecurityGroupIds=[security_group_id],
        DBSubnetGroupName="private_subnets_for_db",
        BackupRetentionPeriod=7,
        # port for mysql 3306
        Port=3306,
        MultiAZ=False,
        EngineVersion='8.0.32',
        AutoMinorVersionUpgrade=True,
        # Iops=123, # Necessary when StorageType is 'io1'
        PubliclyAccessible=True,
        Tags=[
            {
                'Key': 'Name',
                'Value': 'First RDS'
            },
        ],
        MaxAllocatedStorage=100,
        StorageType='gp2',
        # AllowMajorVersionUpgrade=True,
        # EnablePerformanceInsights=True, # performance insights not used with mysql
        # PerformanceInsightsRetentionPeriod=7,
        DeletionProtection=False,
    )

    _id = response.get("DBInstance").get("DBInstanceIdentifier")
    print(f"Instance {_id} was created")

    return response


def modify_mysql_instance(rds_client, rds_identifier, increment):
    """Creates a new RDS instance that is associated with the given security group."""
    response = rds_client.modify_db_instance(
        DBInstanceIdentifier=rds_identifier,
        AllocatedStorage=BASE_MYSQL_STORAGE + increment,
        ApplyImmediately=True,
        AllowMajorVersionUpgrade=True,
        # DBInstanceClass='db.t4g.micro',
        # Engine='mysql',
        # MasterUsername='mysqlusername',
        # MasterUserPassword='mysqlpass',
        # VpcSecurityGroupIds=[security_group_id],
        # DBSubnetGroupName="subnets_for_db",
        # BackupRetentionPeriod=7,
        # port for mysql 3306
        # Port=3306,
        # MultiAZ=False,
        # EngineVersion='8.0.32',
        # AutoMinorVersionUpgrade=True,
        # Iops=123, # Necessary when StorageType is 'io1'
        # PubliclyAccessible=True,
        # Tags=[
        #     {
        #         'Key': 'Name',
        #         'Value': 'First RDS'
        #     },
        # ],
        # StorageType='gp2',
        MaxAllocatedStorage=100,
        # EnablePerformanceInsights=True, # performance insights not used with mysql
        # PerformanceInsightsRetentionPeriod=7,
        # DeletionProtection=False,
    )
    print("RDS Modified!")
    return BASE_MYSQL_STORAGE == BASE_MYSQL_STORAGE + increment


def change_pass_mysql_instance(rds_client, rds_identifier, new_pass):
    """Creates a new RDS instance that is associated with the given security group."""
    if len(new_pass) >= 4:
        response = rds_client.modify_db_instance(
            DBInstanceIdentifier=rds_identifier,
            # DBInstanceClass='db.t4g.micro',
            # Engine='mysql',
            # MasterUsername='mysqlusername',
            MasterUserPassword=new_pass,
            # VpcSecurityGroupIds=[security_group_id],
            # DBSubnetGroupName="subnets_for_db",
            # BackupRetentionPeriod=7,
            # port for mysql 3306
            # Port=3306,
            # MultiAZ=False,
            # EngineVersion='8.0.32',
            # AutoMinorVersionUpgrade=True,
            # Iops=123, # Necessary when StorageType is 'io1'
            # PubliclyAccessible=True,
            # Tags=[
            #     {
            #         'Key': 'Name',
            #         'Value': 'First RDS'
            #     },
            # ],
            # StorageType='gp2',
            # MaxAllocatedStorage=100,
            # EnablePerformanceInsights=True, # performance insights not used with mysql
            # PerformanceInsightsRetentionPeriod=7,
            # DeletionProtection=False,
        )
        print("RDS password Modified!")
        return response
    else:
        print("new password must contain at least 4 characters")


def add_rds_access_sg(sg_id, aws_ec2_client):
    response = aws_ec2_client.authorize_security_group_ingress(
        # CIDRIP="0.0.0.0/0",
        CidrIp="0.0.0.0/0",
        FromPort=3306,
        # EC2SecurityGroupId=sg_id
        GroupId=sg_id,
        IpProtocol='tcp',
        ToPort=3306,
    )
    if response.get("Return"):
        print("http access rule added successfully")
    else:
        print("Rule was not added")


def print_connection_params(rds_client, identifier):
    response = rds_client.describe_db_instances(DBInstanceIdentifier=identifier)
    instance = response.get("DBInstances")[0]
    endpoint = instance.get("Endpoint")
    host = endpoint.get("Address")
    port = endpoint.get("Port")
    username = instance.get("MasterUsername")
    db_name = instance.get("DBName")
    print("DB Host:", host)
    print("DB port:", port)
    print("DB user:", username)
    print("DB database:", db_name)


def reboot_rds(rds_client, identifier):
    rds_client.reboot_db_instance(DBInstanceIdentifier=identifier)
    print(f"RDS - {identifier} rebooted successfully")


def stop_rds(rds_client, identifier):
    response = rds_client.stop_db_instance(
        DBInstanceIdentifier=identifier, DBSnapshotIdentifier="stop-snapshot001")

    print(response)


def start_rds(rds_client, identifier):
    response = rds_client.start_db_instance(DBInstanceIdentifier=identifier)

    print(response)


def update_rds_pass(rds_cient, identifer):
    response = rds_cient.modify_db_instance(DBInstanceIdentifier=identifer,
                                            MasterUserPassword="new-pa$$word")

    print(response)


def delete_rds_pass(rds_cient, identifer):
    response = rds_cient.modify_db_instance(DBInstanceIdentifier=identifer,
                                            MasterUserPassword="new-pa$$word")

    print(response)


def create_db_subnet_group(aws_rds_client, multiple_subnet_id):
    response = aws_rds_client.create_db_subnet_group(
        DBSubnetGroupName='subnets_for_db',
        DBSubnetGroupDescription='subnets_for_db',
        SubnetIds=multiple_subnet_id,
    )
    return response


def create_private_db_subnet_group(aws_rds_client, multiple_subnet_id):
    response = aws_rds_client.create_db_subnet_group(
        DBSubnetGroupName='private_subnets_for_db',
        DBSubnetGroupDescription='private_subnets_for_db',
        SubnetIds=multiple_subnet_id,
    )
    return response


def create_db_snapshot(aws_rds_client, rds_identifier, snap_identifier):
    response = aws_rds_client.create_db_snapshot(
        DBSnapshotIdentifier=snap_identifier,
        DBInstanceIdentifier=rds_identifier,
        Tags=[
            {
                'Key': 'string',
                'Value': snap_identifier
            },
        ]
    )
    print("snapshot made!")
    print(snap_identifier)
    return response


def launch_rds(ec2_client, rds_client, args):
    vpc_id = args.vpc_id
    # create security group for our rds instance
    security_group_id = create_security_group(ec2_client,
                                              "rds-sg", "Security group to enable access on rds", vpc_id)
    # open connection from any ip to rds
    add_rds_access_sg(security_group_id, ec2_client)
    try:
        create_db_subnet_group(rds_client, args.multiple_subnet_id)
    except:
        print("db_subnet_group already exists")
    # create mysql database
    create_mysql_instance(rds_client, security_group_id, args.rds_identifier)


def launch_rds_for_bastion(ec2_client, rds_client, args):
    vpc_id = args.vpc_id
    # create security group for our rds instance
    security_group_id = create_security_group(ec2_client,
                                              "rds-sg", "Security group to enable access on rds", vpc_id)
    # open connection from any ip to rds
    add_rds_access_sg(security_group_id, ec2_client)
    try:
        create_private_db_subnet_group(rds_client, args.multiple_subnet_id)
    except:
        print("db_subnet_group already exists")
    # create mysql database
    create_mysql_instance_for_bastion(rds_client, security_group_id, args.rds_identifier)


def get_rds_details(rds_client, args):
    # test connection to rds instance
    print_connection_params(rds_client, args.rds_identifier)

# def create_bastion_rds(rds_client, args):
#     rds_subnet_group = create_db_subnet_group(rds_client, multiple_subnet_id)
