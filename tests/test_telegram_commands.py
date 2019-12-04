import datetime
import sys
import unittest
from datetime import date
from unittest.mock import Mock

add_to_db_mock = Mock()
delete_from_db_mock = Mock()
db_commands_mock_attrs = {'add_to_db': add_to_db_mock, 'delete_from_db': delete_from_db_mock}

sys.modules['src.db_commands'] = Mock(**db_commands_mock_attrs)


class NewDate(date):
    weekday_result = 0

    @classmethod
    def weekday(cls):
        return cls.weekday_result


datetime.date = NewDate

from src.telegram_commands import handle_command, handle_ordinary_message

del sys.modules['src.db_commands']


class TestHandleOrdinaryMessage(unittest.TestCase):
    def setUp(self):
        self.chat_id = 2

        attrs = {'effective_message.chat_id': self.chat_id}

        self.bot = Mock()
        self.update = Mock(**attrs)

    def test_message_sent(self):
        handle_ordinary_message(self.bot, self.update)

        self.bot.send_message.assert_called_once_with(self.chat_id, 'Вабба-лабба-даб-дабс!')


class TestHandleCommand(unittest.TestCase):
    def setUp(self):
        self.chat_id = 2

        attrs = {'effective_message.chat_id': self.chat_id}

        self.bot = Mock()
        self.update = Mock(**attrs)

    def tearDown(self):
        add_to_db_mock.reset_mock()
        delete_from_db_mock.reset_mock()

    def test_help(self):
        self.update.effective_message.text = '/help'
        handle_command(self.bot, self.update)

        self.bot.send_message.assert_called_once()

    def test_subscribe(self):
        self.update.effective_message.text = '/subscribe'
        handle_command(self.bot, self.update)

        self.bot.send_message.assert_called_once()
        add_to_db_mock.assert_called_once_with(self.chat_id)
        delete_from_db_mock.assert_not_called()

    def test_unsubscribe(self):
        self.update.effective_message.text = '/unsubscribe'
        handle_command(self.bot, self.update)

        self.bot.send_message.assert_called_once()
        add_to_db_mock.assert_not_called()
        delete_from_db_mock.assert_called_once_with(self.chat_id)

    def test_when(self):
        datetime.date.weekday_result = 5
        self.update.effective_message.text = '/when'

        start_string = 'до выхода новой серии '
        end_string = ', озвучка Сыендука выйдет вечером следующего дня'

        handle_command(self.bot, self.update)
        self.bot.send_message.assert_called_with(self.chat_id, start_string + 'остался 1 день' + end_string)

        datetime.date.weekday_result = 4

        handle_command(self.bot, self.update)
        self.bot.send_message.assert_called_with(self.chat_id, start_string + 'осталось 2 дня' + end_string)

        datetime.date.weekday_result = 1

        handle_command(self.bot, self.update)
        self.bot.send_message.assert_called_with(self.chat_id, start_string + 'осталось 5 дней' + end_string)

        datetime.date.weekday_result = 6

        handle_command(self.bot, self.update)
        self.bot.send_message.assert_called_with(self.chat_id, 'Новая серия выходит сегодня')


if __name__ == '__main__':
    unittest.main()
