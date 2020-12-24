# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: H:\workspaces\workspace-python\big-brother-bot\tests\plugins\test_sftpytail.py
# Compiled at: 2015-02-24 17:29:43
import os
from textwrap import dedent
import unittest
from mockito import when, unstub
import b3
from b3.config import CfgConfigParser
from tests import B3TestCase
try:
    import paramiko
except ImportError:
    raise unittest.SkipTest('paramiko module required')

from b3.plugins.sftpytail import SftpytailPlugin

class Test_Sftpytail_plugin(B3TestCase):

    def setUp(self):
        super(Test_Sftpytail_plugin, self).setUp()
        self.conf = CfgConfigParser()
        self.p = SftpytailPlugin(self.console, self.conf)

    def tearDown(self):
        B3TestCase.tearDown(self)
        unstub()


class Test_config_timeout(Test_Sftpytail_plugin):
    DEFAULT_TIMEOUT = 30

    def test_no_setting(self):
        self.conf.loadFromString(dedent('\n            [settings]\n        '))
        self.p.onLoadConfig()
        self.assertEqual(Test_config_timeout.DEFAULT_TIMEOUT, self.p._connectionTimeout)

    def test_nominal(self):
        self.conf.loadFromString(dedent('\n            [settings]\n            timeout: 123\n        '))
        self.p.onLoadConfig()
        self.assertEqual(123, self.p._connectionTimeout)

    def test_empty(self):
        self.conf.loadFromString(dedent('\n            [settings]\n            timeout:\n        '))
        self.p.onLoadConfig()
        self.assertEqual(Test_config_timeout.DEFAULT_TIMEOUT, self.p._connectionTimeout)

    def test_negative(self):
        self.conf.loadFromString(dedent('\n            [settings]\n            timeout: -45\n        '))
        self.p.onLoadConfig()
        self.assertEqual(Test_config_timeout.DEFAULT_TIMEOUT, self.p._connectionTimeout)

    def test_junk(self):
        self.conf.loadFromString(dedent('\n            [settings]\n            timeout: f00\n        '))
        self.p.onLoadConfig()
        self.assertEqual(Test_config_timeout.DEFAULT_TIMEOUT, self.p._connectionTimeout)


class Test_config_maxGapBytes(Test_Sftpytail_plugin):
    DEFAULT_MAXGAPBYTES = 20480

    def test_no_setting(self):
        self.conf.loadFromString(dedent('\n            [settings]\n        '))
        self.p.onLoadConfig()
        self.assertEqual(Test_config_maxGapBytes.DEFAULT_MAXGAPBYTES, self.p._maxGap)

    def test_nominal(self):
        self.conf.loadFromString(dedent('\n            [settings]\n            maxGapBytes: 1234\n        '))
        self.p.onLoadConfig()
        self.assertEqual(1234, self.p._maxGap)

    def test_empty(self):
        self.conf.loadFromString(dedent('\n            [settings]\n            maxGapBytes:\n        '))
        self.p.onLoadConfig()
        self.assertEqual(Test_config_maxGapBytes.DEFAULT_MAXGAPBYTES, self.p._maxGap)

    def test_negative(self):
        self.conf.loadFromString(dedent('\n            [settings]\n            maxGapBytes: -45\n        '))
        self.p.onLoadConfig()
        self.assertEqual(Test_config_maxGapBytes.DEFAULT_MAXGAPBYTES, self.p._maxGap)

    def test_junk(self):
        self.conf.loadFromString(dedent('\n            [settings]\n            maxGapBytes: f00\n        '))
        self.p.onLoadConfig()
        self.assertEqual(Test_config_maxGapBytes.DEFAULT_MAXGAPBYTES, self.p._maxGap)


class Test_config_known_hosts_file(Test_Sftpytail_plugin):

    def test_no_setting(self):
        self.conf.loadFromString(dedent('\n            [settings]\n        '))
        self.p.onLoadConfig()
        self.assertIsNone(self.p.known_hosts_file)

    def test_nominal(self):
        existing_file_path = b3.getAbsolutePath('/a/file/that/exists')
        when(os.path).isfile(existing_file_path).thenReturn(True)
        self.conf.loadFromString(dedent('\n            [settings]\n            known_hosts_file: /a/file/that/exists\n        '))
        self.p.onLoadConfig()
        self.assertIsNotNone(self.p.known_hosts_file)
        self.assertEqual(existing_file_path, b3.getAbsolutePath(self.p.known_hosts_file))

    def test_empty(self):
        self.conf.loadFromString(dedent('\n            [settings]\n            known_hosts_file:\n        '))
        self.p.onLoadConfig()
        self.assertIsNone(self.p.known_hosts_file)

    def test_non_existing_file(self):
        self.conf.loadFromString(dedent('\n            [settings]\n            known_hosts_file: /a/file/that/does/not/exist\n        '))
        self.p.onLoadConfig()
        self.assertIsNone(self.p.known_hosts_file)

    def test_junk(self):
        self.conf.loadFromString(dedent('\n            [settings]\n            known_hosts_file: f00\n        '))
        self.p.onLoadConfig()
        self.assertIsNone(self.p.known_hosts_file)


class Test_config_private_key_file(Test_Sftpytail_plugin):

    def test_no_setting(self):
        self.conf.loadFromString(dedent('\n            [settings]\n        '))
        self.p.onLoadConfig()
        self.assertIsNone(self.p.private_key_file)

    def test_nominal(self):
        existing_file_path = b3.getAbsolutePath('/a/file/that/exists')
        when(os.path).isfile(existing_file_path).thenReturn(True)
        self.conf.loadFromString(dedent('\n            [settings]\n            private_key_file: /a/file/that/exists\n        '))
        self.p.onLoadConfig()
        self.assertIsNotNone(self.p.private_key_file)
        self.assertEqual(existing_file_path, b3.getAbsolutePath(self.p.private_key_file))

    def test_empty(self):
        self.conf.loadFromString(dedent('\n            [settings]\n            private_key_file:\n        '))
        self.p.onLoadConfig()
        self.assertIsNone(self.p.private_key_file)

    def test_non_existing_file(self):
        self.conf.loadFromString(dedent('\n            [settings]\n            private_key_file: /a/file/that/does/not/exist\n        '))
        self.p.onLoadConfig()
        self.assertIsNone(self.p.private_key_file)

    def test_junk(self):
        self.conf.loadFromString(dedent('\n            [settings]\n            private_key_file: f00\n        '))
        self.p.onLoadConfig()
        self.assertIsNone(self.p.private_key_file)


class Test_get_host_keys_file(Test_Sftpytail_plugin):

    def setUp(self):
        Test_Sftpytail_plugin.setUp(self)
        self.p.onLoadConfig()
        self.assertIsNone(self.p.known_hosts_file)
        self.sentinels = {'~/.ssh/known_hosts': object(), 
           '~/ssh/known_hosts': object()}

    def init(self, existing_file_path=None):
        for path, sentinel in self.sentinels.items():
            when(b3).getAbsolutePath(path).thenReturn(sentinel)
            when(os.path).isfile(sentinel).thenReturn(path == existing_file_path)

    def test_fallback_on_user_dot_ssh_directory(self):
        self.init(existing_file_path='~/.ssh/known_hosts')
        self.assertEqual(self.sentinels['~/.ssh/known_hosts'], self.p.get_host_keys_file())

    def test_fallback_on_user_ssh_directory(self):
        self.init(existing_file_path='~/ssh/known_hosts')
        self.assertEqual(self.sentinels['~/ssh/known_hosts'], self.p.get_host_keys_file())

    def test_no_fallback_found(self):
        self.init(existing_file_path=None)
        self.assertIsNone(self.p.get_host_keys_file())
        return