import boto3

client = boto3.client('ssm')


def get_secret(key):
    resp = client.get_parameter(Name=key)

    return resp['Parameter']['Value']
