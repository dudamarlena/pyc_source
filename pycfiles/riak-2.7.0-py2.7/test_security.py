# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: py-build/2.7/bdist.linux-x86_64/egg/riak/tests/test_security.py
# Compiled at: 2016-10-17 19:06:50
import sys, unittest
from riak.tests import RUN_SECURITY, SECURITY_USER, SECURITY_PASSWD, SECURITY_CACERT, SECURITY_KEY, SECURITY_CERT, SECURITY_REVOKED, SECURITY_CERT_USER, SECURITY_BAD_CERT, SECURITY_CIPHERS
from riak.security import SecurityCreds
from riak.tests.base import IntegrationTestBase

class SecurityTests(IntegrationTestBase, unittest.TestCase):

    @unittest.skipIf(RUN_SECURITY, 'RUN_SECURITY is 1')
    def test_security_disabled(self):
        """
        Test valid security settings without security enabled
        """
        topts = {'timeout': 1}
        creds = SecurityCreds(username='foo', password='bar')
        client = self.create_client(credentials=creds, transport_options=topts)
        myBucket = client.bucket('test')
        val1 = 'foobar'
        key1 = myBucket.new('x', data=val1)
        with self.assertRaises(Exception):
            key1.store()
        client.close()

    @unittest.skipUnless(RUN_SECURITY, 'RUN_SECURITY is 0')
    def test_security_basic_connection(self):
        myBucket = self.client.bucket('test')
        val1 = 'foobar'
        key1 = myBucket.new('x', data=val1)
        key1.store()
        myBucket.get('x')

    @unittest.skipUnless(RUN_SECURITY, 'RUN_SECURITY is 0')
    def test_security_bad_user(self):
        creds = SecurityCreds(username='foo', password=SECURITY_PASSWD, cacert_file=SECURITY_CACERT, ciphers=SECURITY_CIPHERS)
        client = self.create_client(credentials=creds)
        with self.assertRaises(Exception):
            client.get_buckets()
        client.close()

    @unittest.skipUnless(RUN_SECURITY, 'RUN_SECURITY is 0')
    def test_security_bad_password(self):
        creds = SecurityCreds(username=SECURITY_USER, password='foo', cacert_file=SECURITY_CACERT, ciphers=SECURITY_CIPHERS)
        client = self.create_client(credentials=creds)
        with self.assertRaises(Exception):
            client.get_buckets()
        client.close()

    @unittest.skipUnless(RUN_SECURITY, 'RUN_SECURITY is 0')
    def test_security_invalid_cert(self):
        creds = SecurityCreds(username=SECURITY_USER, password=SECURITY_PASSWD, cacert_file='/tmp/foo', ciphers=SECURITY_CIPHERS)
        client = self.create_client(credentials=creds)
        with self.assertRaises(Exception):
            client.get_buckets()
        client.close()

    @unittest.skipUnless(RUN_SECURITY, 'RUN_SECURITY is 0')
    def test_security_password_without_cacert(self):
        creds = SecurityCreds(username=SECURITY_USER, password=SECURITY_PASSWD, ciphers=SECURITY_CIPHERS)
        client = self.create_client(credentials=creds)
        with self.assertRaises(Exception):
            myBucket = client.bucket('test')
            val1 = 'foobar'
            key1 = myBucket.new('x', data=val1)
            key1.store()
        client.close()

    @unittest.skipUnless(RUN_SECURITY, 'RUN_SECURITY is 0')
    def test_security_cert_authentication(self):
        creds = SecurityCreds(username=SECURITY_CERT_USER, ciphers=SECURITY_CIPHERS, cert_file=SECURITY_CERT, pkey_file=SECURITY_KEY, cacert_file=SECURITY_CACERT)
        client = self.create_client(credentials=creds)
        myBucket = client.bucket('test')
        val1 = 'foobar2'
        key1 = myBucket.new('x', data=val1)
        if self.protocol == 'pbc':
            key1.store()
            myBucket.get('x')
        else:
            with self.assertRaises(Exception):
                key1.store()
                myBucket.get('x')
        client.close()

    @unittest.skipUnless(RUN_SECURITY, 'RUN_SECURITY is 0')
    def test_security_revoked_cert(self):
        creds = SecurityCreds(username=SECURITY_USER, password=SECURITY_PASSWD, ciphers=SECURITY_CIPHERS, cacert_file=SECURITY_CACERT, crl_file=SECURITY_REVOKED)
        if sys.version_info >= (2, 7, 9):
            return
        client = self.create_client(credentials=creds)
        with self.assertRaises(Exception):
            client.get_buckets()
        client.close()

    @unittest.skipUnless(RUN_SECURITY, 'RUN_SECURITY is 0')
    def test_security_bad_ca_cert(self):
        creds = SecurityCreds(username=SECURITY_USER, password=SECURITY_PASSWD, ciphers=SECURITY_CIPHERS, cacert_file=SECURITY_BAD_CERT)
        client = self.create_client(credentials=creds)
        with self.assertRaises(Exception):
            client.get_buckets()
        client.close()

    @unittest.skipUnless(RUN_SECURITY, 'RUN_SECURITY is 0')
    def test_security_ciphers(self):
        creds = SecurityCreds(username=SECURITY_USER, password=SECURITY_PASSWD, ciphers=SECURITY_CIPHERS, cacert_file=SECURITY_CACERT)
        client = self.create_client(credentials=creds)
        myBucket = client.bucket('test')
        val1 = 'foobar'
        key1 = myBucket.new('x', data=val1)
        key1.store()
        myBucket.get('x')
        client.close()

    @unittest.skipUnless(RUN_SECURITY, 'RUN_SECURITY is 0')
    def test_security_bad_ciphers(self):
        creds = SecurityCreds(username=SECURITY_USER, password=SECURITY_PASSWD, cacert_file=SECURITY_CACERT, ciphers='ECDHE-RSA-AES256-GCM-SHA384')
        client = self.create_client(credentials=creds)
        with self.assertRaises(Exception):
            client.get_buckets()
        client.close()