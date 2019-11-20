import boto3
import telegram

from src.utils import get_secret

dynamodb = boto3.resource('dynamodb', region_name='eu-central-1')

BOT_TOKEN = get_secret('rick-and-morty-token')
bot = telegram.Bot(BOT_TOKEN)


def handler(event, context):
    table = dynamodb.Table('telegram_chats')
    items = table.scan()

    for item in items['Items']:
        bot.send_message(int(item['chat_id']), 'сегодня выходит новая серия, озвучка от Сыендука выходит завтра')
