import boto3
from dotenv import load_dotenv

from os import getenv


def init_rds_client():
    client = boto3.client(
        "rds",
        aws_access_key_id=getenv("aws_access_key_id"),
        aws_secret_access_key=getenv("aws_secret_access_key"),
        aws_session_token=getenv("aws_session_token"),
        region_name=getenv("aws_region_name"))
    return client


load_dotenv()
