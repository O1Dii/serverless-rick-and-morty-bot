import json

import telegram

from src.telegram_commands import handle_command, handle_ordinary_message
from src.utils import get_secret

BOT_TOKEN = get_secret('rick-and-morty-token')
bot = telegram.Bot(BOT_TOKEN)


def handler(event, context):
    response = {
        "statusCode": 200
    }

    update = telegram.Update.de_json(json.loads(event['body']), bot)

    if update.effective_message.text[0] == '/':
        handle_command(bot, update)
    else:
        handle_ordinary_message(bot, update)

    return response
