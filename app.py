import os
import uuid
import json
import boto3
from datetime import datetime


USAGE_TABLE = os.environ["USAGE_TABLE"]
TOKEN = os.environ["TOKEN"]
client = boto3.client("dynamodb")


def app(event, context):
    print(event)
    payload = json.loads(event["body"])
    token = payload.get("token")
    if token != TOKEN:
        return {"statusCode": 500, "body": "token not valid"}

    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    userid = payload.get("userid")
    action = payload.get("action")
    event_name = payload.get("event_name")

    resp = client.put_item(
        TableName=USAGE_TABLE,
        Item={
            'pk': { 'S': str(uuid.uuid4()) },
            'userid': {'S': userid},
            'action': {'S': action},
            'event_name': {'S': event_name},
            'timestamp': {'S': timestamp}
        },
    )

    return {"statusCode": 200, "body": "success"}

