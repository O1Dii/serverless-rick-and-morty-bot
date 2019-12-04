import sys
import unittest
from unittest.mock import Mock

client_mock = Mock(name='client_mock')
sys.modules['boto3'] = Mock(name='boto3_mock', **{'client.return_value': client_mock})

from src.utils import get_secret

del sys.modules['boto3']


class TestUtils(unittest.TestCase):
    def test_get_secret(self):
        key = 2
        value = 'value'

        client_mock.get_parameter.return_value = {'Parameter': {'Value': value}}

        result = get_secret(key)

        client_mock.get_parameter.assert_called_once_with(Name=key)
        self.assertEqual(result, value)


if __name__ == '__main__':
    unittest.main()
