import json
import sys
import unittest
from unittest.mock import Mock

telegram_commands_mock = Mock(name='telegram_commands_mock')
de_json_mock = Mock(name='de_json_mock')
bot_mock = Mock(name='bot_mock')
telegram_mock = Mock(name='telegram_mock', **{'Update.de_json.return_value': de_json_mock,
                                              'Bot.return_value': bot_mock})
sys.modules['telegram'] = telegram_mock
sys.modules['src.telegram_commands'] = telegram_commands_mock
sys.modules['src.utils'] = Mock()

from src.bot_handler import handler

del sys.modules['telegram']
del sys.modules['src.telegram_commands']
del sys.modules['src.utils']


class TestHandler(unittest.TestCase):
    def tearDown(self):
        telegram_mock.reset_mock()
        telegram_commands_mock.reset_mock()

    def test_ordinary_messages(self):
        json_data = '[123, "abc"]'
        converted_json = json.loads(json_data)
        de_json_mock.effective_message.text = '123'

        handler({'body': json_data}, 1)

        telegram_mock.Update.de_json.assert_called_once_with(converted_json, bot_mock)
        telegram_commands_mock.handle_ordinary_message.assert_called_once_with(bot_mock, de_json_mock)

    def test_command(self):
        json_data = '[123, "abc"]'
        converted_json = json.loads(json_data)
        de_json_mock.effective_message.text = '/123'

        handler({'body': json_data}, 1)

        telegram_mock.Update.de_json.assert_called_once_with(converted_json, bot_mock)
        telegram_commands_mock.handle_command.assert_called_once_with(bot_mock, de_json_mock)


if __name__ == '__main__':
    unittest.main()
