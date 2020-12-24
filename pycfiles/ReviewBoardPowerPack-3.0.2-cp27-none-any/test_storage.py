# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /rbpowerpack/sshdb/tests/test_storage.py
# Compiled at: 2019-06-17 15:11:31
from __future__ import unicode_literals
from reviewboard.ssh.errors import UnsupportedSSHKeyError
from rbpowerpack.sshdb.models import StoredHostKeys
from rbpowerpack.sshdb.storage import DBSSHStorage
from rbpowerpack.sshdb.tests.testcases import DBSSHTestCase

class DBSSHStorageTestCase(DBSSHTestCase):

    def test_write_user_key_unsupported(self):
        """Testing DBSSHStorage.write_user_key with unsupported key type"""

        class FakeKey(object):
            pass

        storage = DBSSHStorage()
        self.assertRaises(UnsupportedSSHKeyError, lambda : storage.write_user_key(FakeKey()))

    def test_read_host_keys(self):
        """Testing DBSSHStorage.read_host_keys"""
        storage = DBSSHStorage()
        line1 = b'host1 ssh-rsa %s' % self.key1_b64
        line2 = b'host2 ssh-dss %s' % self.key2_b64
        StoredHostKeys.objects.create(host_keys=(b'').join([
         b'%s\n' % line1,
         b'\n',
         b'# foo\n',
         b'%s  \n' % line2]))
        lines = storage.read_host_keys()
        self.assertEqual(len(lines), 2)
        self.assertEqual(lines[0], line1)
        self.assertEqual(lines[1], line2)

    def test_add_host_key(self):
        """Testing DBSSHStorage.add_host_key"""
        storage = DBSSHStorage()
        storage.add_host_key(b'host1', self.key1)
        stored_host_keys = StoredHostKeys.objects.get()
        lines = stored_host_keys.host_keys.splitlines(True)
        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0], b'host1 ssh-rsa %s\n' % self.key1_b64)

    def test_replace_host_key(self):
        """Testing DBSSHStorage.replace_host_key"""
        storage = DBSSHStorage()
        storage.add_host_key(b'host1', self.key1)
        storage.replace_host_key(b'host1', self.key1, self.key2)
        stored_host_keys = StoredHostKeys.objects.get()
        lines = stored_host_keys.host_keys.splitlines(True)
        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0], b'host1 ssh-dss %s\n' % self.key2_b64)

    def test_replace_host_key_no_known_hosts(self):
        """Testing DBSSHStorage.replace_host_key with no known hosts file"""
        storage = DBSSHStorage()
        storage.replace_host_key(b'host1', self.key1, self.key2)
        stored_host_keys = StoredHostKeys.objects.get()
        lines = stored_host_keys.host_keys.splitlines(True)
        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0], b'host1 ssh-dss %s\n' % self.key2_b64)