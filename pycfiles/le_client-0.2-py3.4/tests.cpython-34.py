# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/le_client/tests.py
# Compiled at: 2016-07-21 14:55:30
# Size of source mod 2**32: 7029 bytes
import unittest
from unittest.mock import Mock, patch, call, ANY
import textwrap, base64, json
from . import ACMEAuthority, ECKeyFile, CertificateRequest

class LeClientTestCase(unittest.TestCase):

    @patch('subprocess.Popen')
    def test_ec_key(self, popen):
        KEY_DUMP = textwrap.dedent('\n            Private-Key: (256 bit)\n            priv:\n                04:00:00:00:00:00:00:00:00:00:00:00:00:00:00:\n                00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:\n                00:01\n            pub:\n                04:00:00:00:00:00:00:00:00:00:00:00:00:00:00:\n                00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:\n                00:00:01:00:00:00:00:00:00:00:00:00:00:00:00:\n                00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:\n                00:00:00:00:02\n            ASN1 OID: prime256v1\n            NIST CURVE: P-256\n        ').strip().encode('ascii')

        def mock_openssl(*whatever):
            return (
             KEY_DUMP, 'wat')

        process = Mock()
        process.communicate = Mock(return_value=mock_openssl())
        process.returncode = 0
        popen.return_value = process
        key = ECKeyFile('mock.pem')
        jwk = key.as_jwk()
        self.assertEqual(jwk, {'kty': 'EC', 
         'crv': 'P-256', 
         'x': 'A' * 42 + 'E', 
         'y': 'A' * 42 + 'I'})

    @patch('subprocess.Popen')
    def test_csr(self, popen):
        CSR_DUMP = textwrap.dedent('\n            Certificate Request:\n                Data:\n                    Version: 0 (0x0)\n                    Subject:\n                    Subject Public Key Info:\n                        Public Key Algorithm: id-ecPublicKey\n                            Public-Key: (256 bit)\n                            pub:\n                                [skipped]\n                            ASN1 OID: prime256v1\n                            NIST CURVE: P-256\n                    Attributes:\n                    Requested Extensions:\n                        X509v3 Subject Alternative Name:\n                            DNS:example.org, DNS:www.example.org\n                Signature Algorithm: ecdsa-with-SHA256\n                     [skipped]\n        ').strip().encode('ascii')

        def mock_openssl(*whatever):
            return (
             CSR_DUMP, 'wat')

        process = Mock()
        process.communicate = Mock(return_value=mock_openssl())
        process.returncode = 0
        popen.return_value = process
        csr = CertificateRequest('mock.csr')
        domains = csr.get_domains()
        self.assertEqual(domains, {'example.org', 'www.example.org'})

    @patch('urllib.request.urlopen')
    def test_registration(self, urlopen):
        key = Mock()
        key.sign = Mock(return_value='MockSignature')

        def mock_urlopen(url, data=None):
            headers = {'Replay-Nonce': 'MockNonce'}
            response = Mock()
            response.status = 200
            if url.endswith('/new-reg'):
                headers['Location'] = 'mock://reg-location'
                response.status = 201
            response.headers = headers
            response.read = Mock(return_value=b'{"mock": true}')
            return response

        urlopen.side_effect = mock_urlopen
        acme = ACMEAuthority(key, base_url='mock://base')
        is_new, location = acme.register()
        urlopen.assert_has_calls([
         call(acme.base_url + '/directory', None),
         call(acme.base_url + '/acme/new-reg', b'"MockSignature"')])
        self.assertTrue(is_new)
        self.assertEqual(location, 'mock://reg-location')

    @patch('builtins.open')
    @patch('urllib.request.urlopen')
    def test_challenge(self, urlopen, fileopen):
        key = Mock()
        key.sign = Mock(return_value='MockSignature')
        challenge_counter = [
         0]

        def mock_urlopen(url, data=None):
            headers = {'Replay-Nonce': 'MockNonce'}
            response = Mock()
            if url.endswith('/new-authz'):
                response.status = 201
                response.read = Mock(return_value=json.dumps({'status': 'pending', 
                 'challenges': [
                                {'status': 'pending', 
                                 'type': 'some-unknown-type-01', 
                                 'uri': 'mock://challenge/wrong-one', 
                                 'token': 'whatever'},
                                {'status': 'pending', 
                                 'type': 'http-01', 
                                 'uri': 'mock://challenge/http-01', 
                                 'token': 'mock-token-01'}], 
                 'combinations': [
                                  [
                                   0], [1]]}).encode('utf-8'))
            else:
                if url.endswith('/challenge/http-01'):
                    response.status = 202
                    c = b'pending' if challenge_counter[0] < 2 else b'valid'
                    response.read = Mock(return_value=b'{"status": "' + c + b'"}')
                    challenge_counter[0] += 1
                else:
                    if url.endswith('/new-cert'):
                        response.status = 201
                        response.read = Mock(return_value=b'MockCertificateBlob')
                    else:
                        response.status = 200
                        response.read = Mock(return_value=b'{}')
            response.headers = headers
            return response

        urlopen.side_effect = mock_urlopen
        csr = Mock()
        csr.get_domains = Mock(return_value={'example.org'})
        csr.as_der = Mock(return_value=b'MockCSRDERData')
        path_maker = Mock(return_value='/tmp/mock/path')
        acme = ACMEAuthority(key, base_url='mock://base')
        with patch('time.sleep') as (sleep):
            certificate = acme.get_certificate(csr, path_maker)
            sleep.assert_has_calls([call(ANY)])
        path_maker.assert_has_calls([call('example.org')])
        fileopen.assert_has_calls([call('/tmp/mock/path/mock-token-01', 'w')])
        self.assertEqual(certificate, '\n'.join([
         '-----BEGIN CERTIFICATE-----',
         base64.b64encode(b'MockCertificateBlob').decode('ascii'),
         '-----END CERTIFICATE-----', '']))


if __name__ == '__main__':
    unittest.main()