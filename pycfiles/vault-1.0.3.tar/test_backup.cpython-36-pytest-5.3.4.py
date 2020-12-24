# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/julio.rama/git/vault-opensource/storage/tests/test_backup.py
# Compiled at: 2020-03-17 15:36:46
# Size of source mod 2**32: 647 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from unittest.mock import patch, Mock
from unittest import TestCase
from storage.tests import fakes
from storage.views import backup
from vault.tests.fakes import fake_request

class TestSwiftBackup(TestCase):

    def setUp(self):
        self.request = fake_request(user=False)
        patch('storage.views.backup.log', Mock(return_value=None)).start()

    def tearDown(self):
        patch.stopall()

    def test_authenticated_config_backup_url(self):
        response = backup.config_backup_container(self.request, 'blah')
        self.assertEqual(response.status_code, 302)