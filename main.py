import argparse
from auth.auth_ec2 import init_ec2_client
from auth.auth_rds import init_rds_client
from create_vpc.vpc_creation import setupVPC
from launch_ec2.ec2_launch import create_ec2
from rds.rds import launch_rds, get_rds_details

parser = argparse.ArgumentParser()
parser.add_argument("-igw", default="False", choices=["True", "False"], required=False)
parser.add_argument("-vpc", "--create_vpc", default="False", choices=["True", "False"], required=False)
parser.add_argument("-priv", "--private_subnets", type=int, nargs="?", required=False)
parser.add_argument("-pub", "--public_subnets", type=int, nargs="?", required=False)
parser.add_argument("-ec2", "--create_ec2", default="False", choices=["True", "False"], required=False)
parser.add_argument("-vid", "--vpc_id", required=False)
parser.add_argument("-sid", "--subnet_id", required=False, nargs="*")
parser.add_argument("-rds", "--rds_type", required=False, choices=["mysql", "postgres", "mariadb", "aurora-mysql"])
parser.add_argument("-rds_i", "--rds_identifier", required=False)
parser.add_argument("-rds_dets", "--get_rds_details", default="False", choices=["True", "False"], required=False)

if __name__ == "__main__":
    ec2_client = init_ec2_client()
    rds_client = init_rds_client()
    args = parser.parse_args()
    if args.create_vpc == "True":
        setupVPC(ec2_client, args)
    if args.vpc_id and args.subnet_id and args.create_ec2 == "True":
        create_ec2(ec2_client, args)
    if args.vpc_id and args.rds_type == "mysql":
        launch_rds(ec2_client, rds_client, args)

    if args.get_rds_details == "True":
        get_rds_details(rds_client, args)
