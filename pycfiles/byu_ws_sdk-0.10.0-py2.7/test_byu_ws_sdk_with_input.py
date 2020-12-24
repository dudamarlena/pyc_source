# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/byu_ws_sdk/test/test_byu_ws_sdk_with_input.py
# Compiled at: 2014-03-14 18:10:42
import unittest, byu_ws_sdk as oit, getpass

def get_input(prompt):
    try:
        _input = raw_input
    except NameError:
        _input = input

    return _input(prompt)


class TestOITWebServicesLibraryInput(unittest.TestCase):

    def test_ws_session(self):
        net_id = get_input('NetId: ')
        password = getpass.getpass()
        res = oit.get_ws_session(net_id, password, verify=False)
        self.assertTrue('personId' in res)

    def test_authorize_request(self):
        apiKey = get_input('API Key: ')
        sharedSecret = getpass.getpass('Shared secret: ')
        headerValue = oit.get_http_authorization_header(apiKey, sharedSecret, oit.KEY_TYPE_API, oit.ENCODING_URL, 'http://www.byu.edu/', '')
        res = oit.authorize_request('http://www.byu.edu/', headerValue, apiKey, sharedSecret, verify=False)
        self.assertTrue(res is not None)
        return


if __name__ == '__main__':
    unittest.main()