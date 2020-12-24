# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/byu_ws_cli/test/test_cli.py
# Compiled at: 2013-08-09 18:49:07
import unittest, byu_ws_sdk as oit, credentials

class TestOITWebServicesLibrary(unittest.TestCase):

    def test_credentials(self):
        self.assertTrue(credentials.key, 'No key supplied in credentials.py')
        self.assertTrue(credentials.shared_secret, 'No shared_secret supplied in credentials.py')
        self.assertTrue(credentials.username, 'No username supplied in credentials.py')
        self.assertTrue(credentials.password, 'No password supplied in credentials.py')

    def test_send_wsSession_request_v1(self):
        wsSession = oit.get_ws_session(credentials.username, credentials.password, 1)
        self.assertTrue('apiKey' in wsSession)
        self.assertTrue(wsSession['apiKey'])
        self.assertTrue('personId' in wsSession)
        self.assertTrue(wsSession['personId'])
        self.assertTrue('expireDate' in wsSession)
        self.assertTrue(wsSession['expireDate'])
        self.assertTrue('sharedSecret' in wsSession)
        self.assertTrue(wsSession['sharedSecret'])
        url = 'https://ws.byu.edu/example/authentication/hmac/services/v1/exampleWS'
        headerValue = oit.get_http_authorization_header(wsSession['apiKey'], wsSession['sharedSecret'], 'WsSession', 'URL', url)
        version, status, headers, response = oit.send_ws_request(url, 'GET', headers={'Authorization': headerValue})
        print version
        self.assertTrue(version)

    def test_send_apiKey_request_v1(self):
        url = 'https://ws.byu.edu/example/authentication/hmac/services/v1/exampleWS'
        headerValue = oit.get_http_authorization_header(credentials.key, credentials.shared_secret, 'API', 'URL', url)
        version, status, headers, response = oit.send_ws_request(url, 'GET', headers={'Authorization': headerValue})
        print version
        self.assertTrue(version)

    def test_get_nonce(self):
        nonce = oit.get_nonce(credentials.key)
        print nonce
        self.assertTrue(nonce['nonceKey'])
        self.assertTrue(nonce['nonceValue'])
        nonce = oit.get_nonce(credentials.key, 'abc')
        print nonce
        self.assertTrue(nonce['nonceKey'])
        self.assertTrue(nonce['nonceValue'])


if __name__ == '__main__':
    unittest.main()