import sys
import unittest
from unittest.mock import Mock, call

bot_mock = Mock(name='bot_mock')
table_mock = Mock(name='table_mock', **{'scan.return_value': {'Items': [{'chat_id': 1}, {'chat_id': 2}]}})
dynamodb_mock = Mock(name='dynamodb_mock', **{'Table.return_value': table_mock})
sys.modules['boto3'] = Mock(name='boto3_mock', **{'resource.return_value': dynamodb_mock})
sys.modules['telegram'] = Mock(**{'Bot.return_value': bot_mock})
sys.modules['src.utils'] = Mock()

from src.notifications_handler import handler

del sys.modules['boto3']
del sys.modules['telegram']
del sys.modules['src.utils']


class TestHandler(unittest.TestCase):
    def test_message_sending(self):
        handler(1, 1)

        calls = [call(1, 'сегодня выходит новая серия, озвучка от Сыендука выходит завтра'),
                 call(2, 'сегодня выходит новая серия, озвучка от Сыендука выходит завтра')]

        dynamodb_mock.Table.assert_called_once()
        table_mock.scan.assert_called_once()
        bot_mock.send_message.assert_has_calls(calls)


if __name__ == '__main__':
    unittest.main()
