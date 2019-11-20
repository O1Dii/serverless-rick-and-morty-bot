from datetime import date

from src.db_commands import add_to_db, delete_from_db


def handle_command(bot, update):
    chat_id = update.effective_message.chat_id
    text = update.effective_message.text

    if text == '/help':
        reply = 'Этот бот создан для отправки уведомлений о новых сериях мультсериала "Рик и Морти"\n\n' + \
                'Доступные комманды:\n' + \
                '/subscribe - Подписаться на рассылку уведомлений о новых эпизодах "Рик и Морти"\n' + \
                '/unsubscribe - Отменить подписку на рассылку уведомлений\n' + \
                '/when - Узнать, через сколько дней выходит новая серия "Рик и Морти"'

        bot.send_message(chat_id, reply)

    if text == '/subscribe':
        bot.send_message(chat_id, 'Вы будете получать уведомления перед выходом новых серий "Рик и Морти"')
        add_to_db(chat_id)

    if text == '/unsubscribe':
        bot.send_message(chat_id, 'Вы успешно отписались от уведомлений о новых сериях "Рик и Морти"')
        delete_from_db(chat_id)

    if text == '/when':
        days_left = 6 - date.today().weekday()

        if days_left:
            result_string = 'до выхода новой серии '

            if days_left == 1:
                result_string += f'остался 1 день'
            if 1 < days_left <= 4:
                result_string += f'осталось {days_left} дня'
            if days_left > 4:
                result_string += f'осталось {days_left} дней'

            result_string += ', озвучка Сыендука выйдет вечером следующего дня'
        else:
            result_string = 'Новая серия выходит сегодня'

        bot.send_message(chat_id, result_string)


def handle_ordinary_message(bot, update):
    bot.send_message(update.effective_message.chat_id, 'Вабба-лабба-даб-дабс!')
