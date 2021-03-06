# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pylxca/test/unittest/test_pylxca_mock.py
# Compiled at: 2020-05-04 06:59:54
# Size of source mod 2**32: 6224 bytes
import sys, argparse
if sys.version_info[:1] == (2, ):
    import mock, unittest
else:
    import unittest2 as unittest
    from unittest import mock
from nose.tools import assert_equals
from nose.tools import assert_raises
from nose.tools import assert_true
from nose.tools import assert_is_instance
import requests
from nose.tools import assert_dict_contains_subset
from requests.exceptions import HTTPError
import pylxca.pylxca_api.lxca_connection as lxca_connection
try:
    from pylxca.pylxca_cmd.lxca_pyshell import *
except Exception as e:
    print('--------------------')
    print('Error:', e)
    print('Sugesstion: Please install pyLXCA before run (try using easy_install pylxca)')
    print('Exiting..')
    print('--------------------')
    sys.exit(-1)

def get_args():
    parser = argparse.ArgumentParser(description='pylxca function tests usage')
    parser.add_argument('-l', action='store', dest='lxca_ip', required=True, help='Store LXCA IP value')
    parser.add_argument('-n', action='store_false', default=True, dest='no_verify', help='Set a no_verify to false')
    parser.add_argument('-u', action='store', dest='user', type=str, default='USER', help='Specify username. default:"USER"')
    parser.add_argument('-p', action='store', dest='password', type=str, default='PASSWORD', help='Specify password. default: "PASSWORD" ')
    return parser.parse_args()


class MockResponse:

    def __init__(self, json_data, status_code):
        self.text = json_data
        self.status_code = status_code

    def text(self):
        return self.text

    def raise_for_status(self):
        pass


class TestPylxcaApi(unittest.TestCase):
    if __name__ == '__main__':
        arg = get_args()
        _ip = arg.lxca_ip
        _user = arg.user
        _passwd = arg.password
        _noverify = 'True' if arg.no_verify else 'False'
    else:
        _ip = 'LXCA_IP'
        _user = 'LXCA_USER'
        _passwd = 'LXCA_PASSWORD'
        _noverify = 'True'

    @classmethod
    def setUpClass(self):
        pass

    def setUp(self):
        pass

    @mock.patch('pylxca.pylxca.pylxca_api.lxca_connection.test_connection', autospec=True)
    @mock.patch('pylxca.pylxca.pylxca_api.lxca_connection.connect', autospec=True)
    def test__connect_mock(self, connect_mock, test_connection_mock):
        connect_mock.return_value = True
        test_connection_mock.return_value = True
        con = connect(self._ip, self._user, self._passwd, self._noverify)
        print(con)
        assert_is_instance(con, lxca_connection, 'Is not Connection object')

    @mock.patch('pylxca.pylxca.pylxca_cmd.lxca_pyshell.nodes', autospec=True)
    def test__nodes_mock(self, nodes):
        con = con = connect(self._ip, self._user, self._passwd, self._noverify)
        print(con)
        node_dict = {'nodeList': []}
        nodes.return_value = node_dict
        ret_nodes = nodes(con)
        print(ret_nodes)
        assert_equals(ret_nodes, node_dict)

    @mock.patch('pylxca.pylxca.pylxca_api.lxca_rest.get_nodes', autospec=True)
    def test__nodes_rest_mock(self, get_nodes):
        con = connect(self._ip, self._user, self._passwd, self._noverify)
        print(con)
        resp = MockResponse('{"nodeList": []}', 200)
        get_nodes.return_value = resp
        ret_nodes = nodes(con)
        print(ret_nodes)
        assert_equals(ret_nodes['nodeList'], [])

    @mock.patch('pylxca.pylxca.pylxca_api.lxca_rest.get_nodes', autospec=True)
    def test__nodes_rest_mock_exception(self, get_nodes):
        con = connect(self._ip, self._user, self._passwd, self._noverify)
        print(con)
        resp = MockResponse('{"nodeList": []}', 200)
        get_nodes.side_effect = Exception("Invalid argument 'status'")
        get_nodes.return_value = resp
        assert_raises(Exception, nodes, con)

    def test__nodes_invalid_status_exception(self):
        con = con = connect(self._ip, self._user, self._passwd, self._noverify)
        assert_raises(Exception, nodes, con, None, None, 'unknown')

    @mock.patch.object(requests, 'get')
    def test__nodes_valid_status(self, request_get):
        request_get.return_value = MockResponse('{"nodeList": []}', 200)
        con = connect(self._ip, self._user, self._passwd, self._noverify)
        try:
            nodes(con, None, None, 'managed')
        except:
            assert_true(False, ' Got exception and not expecting it')

        assert_true(True, ' No Exception')

    @mock.patch('requests.session')
    def test_should_mock_session_get(self, session_mock):
        session_mock.return_value = mock.MagicMock(get=mock.MagicMock(return_value=(MockResponse('{"nodeList": []}', 200))))
        con = connect(self._ip, self._user, self._passwd, self._noverify)
        try:
            nodes(con, None, None, 'managed')
        except Exception as e:
            print(str(e))
            assert_true(False, ' Got exception and not expecting it')

        assert_true(True, ' No Exception')


if __name__ == '__main__':
    tests = [
     TestPylxcaApi]
    for test in tests:
        suite = unittest.TestLoader().loadTestsFromTestCase(test)
        unittest.TextTestRunner(verbosity=2).run(suite)