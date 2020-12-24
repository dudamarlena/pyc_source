# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mass/PythonProjects/oideas/oideas/accounts/tests/test_authentication.py
# Compiled at: 2015-08-15 23:38:45
# Size of source mod 2**32: 566 bytes
from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from unittest.mock import patch

class ExpiringTokenAuthentication(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()

    @patch('accounts.authentication.ExpiringTokenAuthentication')
    def test_raises_exception_with_wrong_token(self, mock_authentication):
        request = self.factory.get('/', HTTP_AUTHORIZATION='Token FalseToken')
        import pdb
        pdb.set_trace()
        self.assertIs(mock_authentication.called, True)