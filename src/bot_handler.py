import json

from src.telegram_commands import handle_command, handle_ordinary_message


def handler(event, context):
    response = {
        "statusCode": 200
    }

    message = json.loads(event['body']).get('message')

    if not message:
        return response

    if message['text'][0] == '/':
        handle_command(message)
    else:
        handle_ordinary_message(message)

    return response
