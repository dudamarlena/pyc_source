# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/egnyte/tests/test_users.py
# Compiled at: 2017-03-15 09:46:43
from egnyte import configuration, client
import unittest
CONFIG_NAME = 'test_config.json'
USERNAME = 'python_sdk_test_user'
EXTERNAL_ID = 'python_sdk_test_user'
EMAIL = 'python_sdk_test_user@example.com'
ANOTHER_EMAIL = 'python_sdk_another_email@example.com'
FAMILY_NAME = 'Doe'
GIVEN_NAME = 'John'
ACTIVE = False
SEND_INVITE = False

class TestUserInfo(unittest.TestCase):

    def test_userinfo(self):
        self.config = configuration.load(CONFIG_NAME)
        self.egnyte = client.EgnyteClient(self.config)
        data = self.egnyte.user_info
        self.assertEqual(data['username'], self.config['login'], 'Username received from API does not match one in config file')


class TestUsers(unittest.TestCase):

    def setUp(self):
        self.config = configuration.load(CONFIG_NAME)
        self.egnyte = client.EgnyteClient(self.config)
        self.users = self.egnyte.users
        self.user = self.__create_user(self.users)

    def tearDown(self):
        self.user.delete()

    def test_list_users(self):
        all_users = self.egnyte.users.list()
        self.assertGreaterEqual(all_users, 1)

    def test_create_user(self):
        user_by_email = self.users.by_email(EMAIL)
        self.assertEqual(self.user, user_by_email, 'Should find user by email')
        user_by_username = self.users.by_username(USERNAME)
        self.assertEqual(self.user, user_by_username, 'Should find user by username')

    def test_update_user(self):
        self.user.update(email=ANOTHER_EMAIL)
        user_updated = self.users.by_email(EMAIL)
        self.assertIsNone(user_updated, 'Should not find user after email has changed')
        user_updated = self.users.by_email(ANOTHER_EMAIL)
        self.assertEqual(self.user, user_updated, 'Should find user by new email')

    def __create_user(self, users):
        return users.create(userName=USERNAME, externalId=EXTERNAL_ID, email=EMAIL, familyName=FAMILY_NAME, givenName=GIVEN_NAME, active=False, sendInvite=False)