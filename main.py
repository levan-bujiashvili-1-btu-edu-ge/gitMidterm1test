import argparse
import boto3
from dotenv import load_dotenv

from os import getenv

parser = argparse.ArgumentParser()
parser.add_argument("-igw")
parser.add_argument("-vpc", "--create_vpc")

load_dotenv()


def init_client():
    client = boto3.client(
        "ec2",
        aws_access_key_id=getenv("aws_access_key_id"),
        aws_secret_access_key=getenv("aws_secret_access_key"),
        aws_session_token=getenv("aws_session_token"),
        region_name=getenv("aws_region_name"))
    return client


def create_vpc(ec2_client):
    result = ec2_client.create_vpc(CidrBlock="10.0.0.0/16")
    vpc = result.get("Vpc")
    print(vpc)
    return vpc.get("VpcId")


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


if __name__ == "__main__":
    ec2_client = init_client()
    args = parser.parse_args()
    if args.create_vpc:
        vpc_id = create_vpc(ec2_client)
        add_name_tag(vpc_id, ec2_client)
        if args.igw:
            my_igw = create_igw(ec2_client)
            attach_igw_to_vpc(vpc_id, my_igw, ec2_client)
