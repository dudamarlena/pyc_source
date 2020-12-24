# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\sftpytail\test_get_host_keys_file.py
# Compiled at: 2016-03-08 18:42:10
import b3, os
from mockito import when
from tests.plugins.sftpytail import Test_Sftpytail_plugin

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