# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/thevpncompany/test/test_zabbix.py
# Compiled at: 2019-07-29 21:33:05
# Size of source mod 2**32: 2325 bytes
import unittest
from unittest.mock import patch, mock_open, MagicMock
import json, logging, os
from ..zabbix_openvpn_user_discovery import find_openvpn_current_users
from ..zabbix_openvpn_usage_per_user import find_openvpn_data_user
log = logging.getLogger(__name__)
MOCK_USER_DATA_USER1 = 'CLIENT_LIST\t1\t49.195.124.134:64225\t192.168.255.6\t\t2984093\t17687746\tThu Jul 18 03:31:11 2019\t1563420671\tUNDEF\t10\t0\nCLIENT_LIST\t1\t49.195.124.134:64226\t192.168.255.10\t\t41893\t42003\tThu Jul 18 03:31:11 2019\t1563420671\tUNDEF\t11\t1\n'
MOCK_USER_DISCOVERY = 'CLIENT_LIST\t1\t49.195.28.171:43884\t192.168.255.6\t\t8063733\t22005266\tWed Jul 24 23:23:39 2019\t1564010619\tUNDEF\t3\t0\nCLIENT_LIST\t2\t49.195.28.171:43884\t192.168.255.6\t\t8063733\t22005266\tWed Jul 24 23:23:39 2019\t1564010619\tUNDEF\t3\t1\n'

def mock_redis_get_none(*args, **kwargs):
    pass


def mock_redis_get(*args, **kwargs):
    return '{"timestamp": "2019-07-25 11:57:50", "total_session_sent_bytes": 17729749, "total_sent_bytes": 17729749}'.encode('utf-8')


class TestOpenVPNUserDiscovery(unittest.TestCase):

    @patch('subprocess.getoutput', return_value=MOCK_USER_DISCOVERY)
    def test_discover_openvpn_users(self, mock_post):
        """
        Test the zabbix user discovery
        """
        result = find_openvpn_current_users()
        self.assertEqual([{'{#ID}': '1'}, {'{#ID}': '2'}], result)


class TestOpenVPNUserData(unittest.TestCase):

    @patch('subprocess.getoutput', return_value=MOCK_USER_DATA_USER1)
    @patch('redis.Redis.get', side_effect=mock_redis_get_none)
    def test_get_user_data(self, mock_post, mock_redis_get):
        """
        Fetch user bandwidth usage
        """
        with patch('configparser.ConfigParser.read', MagicMock(return_value={})):
            result = find_openvpn_data_user('1')
        self.assertEqual(17729749, result)

    @patch('subprocess.getoutput', return_value=MOCK_USER_DATA_USER1)
    @patch('redis.Redis.get', side_effect=mock_redis_get)
    def test_get_user_data_no_new_traffic(self, mock_post, mock_redis_get):
        """
        Fetch user bandwidth usage
        """
        result = find_openvpn_data_user('1')
        self.assertEqual(0, result)


if __name__ == '__main__':
    unittest.main()