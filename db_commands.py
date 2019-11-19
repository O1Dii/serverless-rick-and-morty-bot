import os

import boto3

TABLE_NAME = os.getenv('table_name')

dynamodb = boto3.resource('dynamodb', region_name='eu-central-1')
table = dynamodb.Table(TABLE_NAME)


def delete_from_db(chat_id):
    table.delete_item(Key={'chat_id': chat_id})


def add_to_db(chat_id):
    table.put_item(Item={'chat_id': chat_id})
