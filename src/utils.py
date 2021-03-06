import boto3

client = boto3.client('ssm')


def get_secret(key):
    return client.get_parameter(Name=key)['Parameter']['Value']
