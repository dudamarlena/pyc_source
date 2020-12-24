# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /rbpowerpack/sshdb/tests/test_client.py
# Compiled at: 2019-06-17 15:11:31
from __future__ import unicode_literals
import tempfile
from reviewboard.ssh.client import SSHClient
from rbpowerpack.sshdb.models import StoredHostKeys, StoredUserKey
from rbpowerpack.sshdb.tests.testcases import DBSSHTestCase

class SSHClientTests(DBSSHTestCase):
    """Unit tests for SSHClient with sshdb."""

    def setUp(self):
        super(SSHClientTests, self).setUp()
        self.tempdir = tempfile.mkdtemp(prefix=b'rb-tests-home-')

    def test_generate_user_key(self, namespace=None):
        """Testing SSHClient.generate_user_key"""
        client = SSHClient(namespace=namespace)
        client.generate_user_key(bits=1024)
        stored_keys = StoredUserKey.objects.all()
        self.assertEqual(len(stored_keys), 1)
        stored_key = stored_keys[0]
        self.assertEqual(stored_key.namespace, namespace)
        self.assertEqual(stored_key.key_type, b'rsa')
        self.assertEqual(client.get_user_key(), stored_key.get_key())

    def test_generate_user_key_with_localsite(self):
        """Testing SSHClient.generate_user_key with localsite"""
        self.test_generate_user_key(b'site-1')

    def test_delete_user_key(self, namespace=None):
        """Testing SSHClient.delete_user_key"""
        client = SSHClient(namespace=namespace)
        client.import_user_key(self.key1)
        stored_keys = StoredUserKey.objects.filter(namespace=namespace)
        self.assertEqual(len(stored_keys), 1)
        self.assertEqual(client.get_user_key(), self.key1)
        client.delete_user_key()
        stored_keys = StoredUserKey.objects.filter(namespace=namespace)
        self.assertEqual(len(stored_keys), 0)

    def test_delete_user_key_with_localsite(self):
        """Testing SSHClient.delete_user_key with localsite"""
        self.test_delete_user_key(b'site-1')

    def test_add_host_key(self, namespace=None):
        """Testing SSHClient.add_host_key"""
        client = SSHClient(namespace=namespace)
        client.add_host_key(b'example.com', self.key1)
        stored_host_keys = StoredHostKeys.objects.get()
        lines = stored_host_keys.host_keys.splitlines(True)
        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0].split(), [
         b'example.com', self.key1.get_name(), self.key1_b64])

    def test_add_host_key_with_localsite(self):
        """Testing SSHClient.add_host_key with localsite"""
        self.test_add_host_key(b'site-1')

    def test_replace_host_key(self, namespace=None):
        """Testing SSHClient.replace_host_key"""
        client = SSHClient(namespace=namespace)
        client.add_host_key(b'example.com', self.key1)
        client.replace_host_key(b'example.com', self.key1, self.key2)
        stored_host_keys = StoredHostKeys.objects.get()
        lines = stored_host_keys.host_keys.splitlines(True)
        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0].split(), [
         b'example.com', self.key2.get_name(),
         self.key2_b64])

    def test_replace_host_key_with_localsite(self):
        """Testing SSHClient.replace_host_key with localsite"""
        self.test_replace_host_key(b'site-1')

    def test_import_user_key(self, namespace=None):
        """Testing SSHClient.import_user_key"""
        client = SSHClient(namespace=namespace)
        client.import_user_key(self.key1)
        self.assertEqual(client.get_user_key(), self.key1)

    def test_import_user_key_with_localsite(self):
        """Testing SSHClient.import_user_key with localsite"""
        self.test_import_user_key(b'site-1')