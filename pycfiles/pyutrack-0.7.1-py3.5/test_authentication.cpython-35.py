# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/integration/test_authentication.py
# Compiled at: 2017-10-28 23:27:23
# Size of source mod 2**32: 700 bytes
from pyutrack import Connection
from pyutrack import Credentials
from pyutrack.errors import LoginError
from tests.integration import IntegrationTest

class AuthenticationTests(IntegrationTest):

    def test_successful_authentication(self):
        connection = Connection(credentials=Credentials(username='root', password='root'), base_url='http://localhost:9876')
        self.assertTrue(connection.login())

    def test_invalid_password(self):
        connection = Connection(credentials=Credentials(username='root', password='rooted'), base_url='http://localhost:9876')
        self.assertRaises(LoginError, connection.login)