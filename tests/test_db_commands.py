import unittest
from unittest.mock import Mock, call

import sys


table_mock = Mock(name='table_mock')
dynamodb_mock = Mock(name='dynamodb_mock', **{'Table.return_value': table_mock})
sys.modules['boto3'] = Mock(name='boto3_mock', **{'resource.return_value': dynamodb_mock})

from src.db_commands import add_to_db, delete_from_db


class TestDbCommands(unittest.TestCase):
    def setUp(self):
        self.chat_id = 1

    def test_delete_from_db(self):
        delete_from_db(self.chat_id)

        table_mock.delete_item.assert_called_once()
        table_mock.reset_mock()

    def test_add_to_db(self):
        add_to_db(self.chat_id)

        table_mock.put_item.assert_called_once_with(Item={'chat_id': self.chat_id})
        table_mock.reset_mock()


if __name__ == '__main__':
    unittest.main()
