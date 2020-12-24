# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-4yaip7h6/keyring/keyring/tests/test_backend.py
# Compiled at: 2016-12-29 05:40:26
# Size of source mod 2**32: 5064 bytes
"""
Common test functionality for backends.
"""
from __future__ import unicode_literals
import string, pytest
from .util import random_string
from keyring import errors
UNICODE_CHARS = 'זהכיףסתםלשמועאיךתנצחקרפדעץטובבגןξεσκεπάζωτηνψυχοφθόραβδελυγμίαСъешьжеещёэтихмягкихфранцузскихбулокдавыпейчаюЖълтатадюлябешещастливачепухъткойтоцъфназамръзнакатогьон'
assert min(ord(char) for char in UNICODE_CHARS) > 127

def is_ascii_printable(s):
    return all(32 <= ord(c) < 127 for c in s)


class BackendBasicTests(object):
    __doc__ = "Test for the keyring's basic functions. password_set and password_get\n    "
    DIFFICULT_CHARS = string.whitespace + string.punctuation

    def setUp(self):
        self.keyring = self.init_keyring()
        self.credentials_created = set()

    def tearDown(self):
        for item in self.credentials_created:
            self.keyring.delete_password(*item)

    def set_password(self, service, username, password):
        self.keyring.set_password(service, username, password)
        self.credentials_created.add((service, username))

    def check_set_get(self, service, username, password):
        keyring = self.keyring
        assert keyring.get_password(service, username) is None
        self.set_password(service, username, password)
        assert keyring.get_password(service, username) == password
        self.set_password(service, username, '')
        assert keyring.get_password(service, username) == ''

    def test_password_set_get(self):
        password = random_string(20)
        username = random_string(20)
        service = random_string(20)
        self.check_set_get(service, username, password)

    def test_difficult_chars(self):
        password = random_string(20, self.DIFFICULT_CHARS)
        username = random_string(20, self.DIFFICULT_CHARS)
        service = random_string(20, self.DIFFICULT_CHARS)
        self.check_set_get(service, username, password)

    def test_delete_present(self):
        password = random_string(20, self.DIFFICULT_CHARS)
        username = random_string(20, self.DIFFICULT_CHARS)
        service = random_string(20, self.DIFFICULT_CHARS)
        self.keyring.set_password(service, username, password)
        self.keyring.delete_password(service, username)
        assert self.keyring.get_password(service, username) is None

    def test_delete_not_present(self):
        username = random_string(20, self.DIFFICULT_CHARS)
        service = random_string(20, self.DIFFICULT_CHARS)
        with pytest.raises(errors.PasswordDeleteError):
            self.keyring.delete_password(service, username)

    def test_delete_one_in_group(self):
        username1 = random_string(20, self.DIFFICULT_CHARS)
        username2 = random_string(20, self.DIFFICULT_CHARS)
        password = random_string(20, self.DIFFICULT_CHARS)
        service = random_string(20, self.DIFFICULT_CHARS)
        self.keyring.set_password(service, username1, password)
        self.set_password(service, username2, password)
        self.keyring.delete_password(service, username1)
        assert self.keyring.get_password(service, username2) == password

    def test_name_property(self):
        assert is_ascii_printable(self.keyring.name)

    def test_unicode_chars(self):
        password = random_string(20, UNICODE_CHARS)
        username = random_string(20, UNICODE_CHARS)
        service = random_string(20, UNICODE_CHARS)
        self.check_set_get(service, username, password)

    def test_unicode_and_ascii_chars(self):
        source = random_string(10, UNICODE_CHARS) + random_string(10) + random_string(10, self.DIFFICULT_CHARS)
        password = random_string(20, source)
        username = random_string(20, source)
        service = random_string(20, source)
        self.check_set_get(service, username, password)

    def test_different_user(self):
        """
        Issue #47 reports that WinVault isn't storing passwords for
        multiple users. This test exercises that test for each of the
        backends.
        """
        keyring = self.keyring
        self.set_password('service1', 'user1', 'password1')
        self.set_password('service1', 'user2', 'password2')
        assert keyring.get_password('service1', 'user1') == 'password1'
        assert keyring.get_password('service1', 'user2') == 'password2'
        self.set_password('service2', 'user3', 'password3')
        assert keyring.get_password('service1', 'user1') == 'password1'