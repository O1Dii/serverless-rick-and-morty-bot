import boto3
import requests

from src.utils import get_secret

dynamodb = boto3.resource('dynamodb', region_name='eu-central-1')

BOT_TOKEN = get_secret('rick-and-morty-token')
BASE_URL = f'https://api.telegram.org/bot{BOT_TOKEN}/'


def send_message(chat_id):
    url = BASE_URL + 'sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': 'сегодня выходит новая серия, озвучка от Сыендука выходит завтра'
    }

    r = requests.post(url, json=payload)

    return r.json()


def handler(event, context):
    table = dynamodb.Table('telegram_chats')
    items = table.scan()

    for item in items['Items']:
        send_message(int(item['chat_id']))
