# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_userchecker.py
# Compiled at: 2011-05-02 14:52:14
"""
Tests for the repoze.who SQLAlchemy MD provider.

"""
import unittest
from repoze.who.plugins.sa import SQLAlchemyUserChecker
import databasesetup_sa
from fixture import sa_model

class TestUserChecker(unittest.TestCase):
    """Tests for the user checker"""

    def setUp(self):
        databasesetup_sa.setup_database()
        self.plugin = SQLAlchemyUserChecker(sa_model.User, sa_model.DBSession)

    def tearDown(self):
        databasesetup_sa.teardownDatabase()

    def test_existing_user(self):
        self.assertTrue(self.plugin('guido'))

    def test_non_existing_user(self):
        self.assertFalse(self.plugin('gustavo'))