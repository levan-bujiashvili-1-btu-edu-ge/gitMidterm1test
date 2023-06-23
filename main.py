import argparse
from auth.auth_ec2 import init_ec2_client
from auth.auth_rds import init_rds_client
from auth.auth_s3 import init_s3_client
from bucket.bucket import upload_file_to_s3
from create_vpc.vpc_creation import setupVPC, create_private_subnet
from dynamo_db.dynamo_db import list_all_local_tables
from launch_ec2.ec2_launch import create_ec2, create_bastion_host, give_access_to_ssh_sg
from my_arguments import ec2_arguments, vpc_arguments, rds_arguments, dynamo_db_arguments, bastion_arguments, \
    bucket_arguments
from rds.rds import launch_rds, get_rds_details, modify_mysql_instance, create_db_snapshot, change_pass_mysql_instance

parser = argparse.ArgumentParser()

subparsers = parser.add_subparsers(dest='command')

ec2 = ec2_arguments(subparsers.add_parser("ec2", help="work with ec2/s"))
vpc = vpc_arguments(subparsers.add_parser("vpc", help="work with vpc/s"))
rds = rds_arguments(subparsers.add_parser("rds", help="work with rds"))
bucket = \
    bucket_arguments(subparsers.add_parser("bucket", help="work with rds"))
dynamo_db = dynamo_db_arguments(subparsers.add_parser("dynamo_db", help="work with dynamo_db"))
bastion_host = bastion_arguments(subparsers.add_parser("bastion_host", help="work with bastion host"))


if __name__ == "__main__":
    ec2_client = init_ec2_client()
    rds_client = init_rds_client()
    s3_client = init_s3_client()
    args = parser.parse_args()

    match args.command:
        case "vpc":
            if args.create_vpc == "True":
                setupVPC(args)
            if args.vpc_id and args.create_private_subnet:
                create_private_subnet(args.vpc_id, args.create_private_subnet, ec2_client)
        case "ec2":
            if args.vpc_id and args.subnet_id and args.create_ec2 == "True":
                create_ec2(ec2_client, args)
            if args.sg_id and args.ssh_my_ip:
                give_access_to_ssh_sg(ec2_client, args.sg_id)
        case "rds":
            if args.vpc_id and args.rds_type == "mysql":
                launch_rds(ec2_client, rds_client, args)

            if args.get_rds_details == "True":
                get_rds_details(rds_client, args)
            if args.rds_identifier and args.storage_increase and args.modify_rds == "True":
                modify_mysql_instance(rds_client, args.rds_identifier, args.storage_increase)

            if args.make_snapshot == "True" and args.snap_identifier and args.rds_identifier:
                create_db_snapshot(rds_client, args.rds_identifier, args.snap_identifier)

            if args.new_pass and args.dbInstanceId:
                change_pass_mysql_instance(rds_client,args.dbInstanceId, args.new_pass)
        case "dynamo_db":
            if args.list_tables == "True":
                list_all_local_tables()

        case "bastion_host":
            if args.vpc_id and args.subnet_id and args.create_bastion_host == "True" and args.rds_type == "mysql":
                create_bastion_host(ec2_client, args)
                launch_rds(ec2_client, rds_client, args)

        case "bucket":
            if args.bucket_name and args.upload_file:
                upload_file_to_s3(s3_client, args.bucket_name, args.upload_file)


