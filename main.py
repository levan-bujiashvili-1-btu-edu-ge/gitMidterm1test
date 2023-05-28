import argparse
from auth.auth_ec2 import init_ec2_client
from create_vpc.vpc_creation import setupVPC
from launch_ec2.ec2_launch import create_ec2


parser = argparse.ArgumentParser()
parser.add_argument("-igw", default="False", choices=["True", "False"], required=False)
parser.add_argument("-vpc", "--create_vpc", default="False", choices=["True", "False"], required=False)
parser.add_argument("-priv", "--private_subnets", type=int, nargs="?", required=False)
parser.add_argument("-pub", "--public_subnets", type=int, nargs="?", required=False)
parser.add_argument("-vid", "--vpc_id", required=False)
parser.add_argument("-sid", "--subnet_id", required=False)


if __name__ == "__main__":
    ec2_client = init_ec2_client()
    args = parser.parse_args()
    if args.create_vpc == "True":
        setupVPC(ec2_client, args)
    if args.vpc_id and args.subnet_id:
        create_ec2(ec2_client, args)
