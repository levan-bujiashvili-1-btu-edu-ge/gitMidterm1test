from os import getenv

import boto3


def list_all_local_tables():
    db = boto3.resource('dynamodb', region_name=getenv("aws_region_name"))
    tables = list(db.tables.all())
    print("dynamoDB tables in this region:\n*********************")
    for i in tables:
        print(i.name)
    print("*********************")
