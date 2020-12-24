# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_mdprovider.py
# Compiled at: 2011-05-02 14:52:14
"""
Tests for the repoze.who SQLAlchemy MD provider.

"""
import unittest
from repoze.who.interfaces import IMetadataProvider
try:
    from sqlalchemy.exceptions import IntegrityError
except ImportError:
    from sqlalchemy.exc import IntegrityError

from zope.interface.verify import verifyClass
from repoze.who.plugins.sa import SQLAlchemyUserMDPlugin, make_sa_user_mdprovider
import databasesetup_sa
from fixture import sa_model

class TestMDProvider(unittest.TestCase):
    """Tests for the authenticator function"""

    def setUp(self):
        databasesetup_sa.setup_database()
        self.plugin = SQLAlchemyUserMDPlugin(sa_model.User, sa_model.DBSession)

    def tearDown(self):
        databasesetup_sa.teardownDatabase()

    def test_implements(self):
        verifyClass(IMetadataProvider, SQLAlchemyUserMDPlugin, tentative=True)

    def test_it(self):
        user = sa_model.DBSession.query(sa_model.User).filter(sa_model.User.user_name == 'rms').one()
        identity = {'repoze.who.userid': user.user_name}
        expected_identity = {'repoze.who.userid': user.user_name, 
           'user': user}
        self.plugin.add_metadata(None, identity)
        self.assertEqual(identity.keys(), expected_identity.keys())
        self.assertEqual(expected_identity['repoze.who.userid'], identity['repoze.who.userid'])
        self.assertEqual(expected_identity['user'].user_name, identity['user'].user_name)
        return

    def test_rollback(self):
        """The session must be rolled back before use."""
        try:
            user = sa_model.User()
            user.user_name = 'rms'
            user.password = 'free software'
            sa_model.DBSession.add(user)
            sa_model.DBSession.commit()
        except IntegrityError:
            pass
        else:
            self.fail("An IntegrityError must've been raised")

        identity = {'repoze.who.userid': 'rms'}
        self.plugin.add_metadata(None, identity)
        return


class TestMDProviderWithTranslations(unittest.TestCase):
    """Tests for the translation functionality"""

    def setUp(self):
        databasesetup_sa.setup_database_with_translations()

    def tearDown(self):
        databasesetup_sa.teardownDatabase()

    def test_it(self):
        self.plugin = SQLAlchemyUserMDPlugin(sa_model.Member, sa_model.DBSession)
        self.plugin.translations['user_name'] = 'member_name'
        member = sa_model.DBSession.query(sa_model.Member).filter(sa_model.Member.member_name == 'rms').one()
        identity = {'repoze.who.userid': member.member_name}
        expected_identity = {'repoze.who.userid': member.member_name, 
           'user': member}
        self.plugin.add_metadata(None, identity)
        self.assertEqual(expected_identity.keys(), identity.keys())
        self.assertEqual(expected_identity['repoze.who.userid'], identity['repoze.who.userid'])
        self.assertEqual(expected_identity['user'].member_name, identity['user'].member_name)
        return


class TestMDProviderMaker(unittest.TestCase):

    def setUp(self):
        databasesetup_sa.setup_database()

    def tearDown(self):
        databasesetup_sa.teardownDatabase()

    def test_simple_call(self):
        user_class = 'tests.fixture.sa_model:User'
        dbsession = 'tests.fixture.sa_model:DBSession'
        mdprovider = make_sa_user_mdprovider(user_class, dbsession)
        self.assertTrue(isinstance(mdprovider, SQLAlchemyUserMDPlugin))

    def test_no_user_class(self):
        dbsession = 'tests.fixture.sa_model:DBSession'
        self.assertRaises(ValueError, make_sa_user_mdprovider, None, dbsession)
        return

    def test_no_dbsession(self):
        user_class = 'tests.fixture.sa_model:User'
        self.assertRaises(ValueError, make_sa_user_mdprovider, user_class)

    def test_username_translation(self):
        user_class = 'tests.fixture.sa_model:User'
        dbsession = 'tests.fixture.sa_model:DBSession'
        username_translation = 'username'
        mdprovider = make_sa_user_mdprovider(user_class, dbsession, username_translation)
        self.assertTrue(isinstance(mdprovider, SQLAlchemyUserMDPlugin))
        self.assertEqual(username_translation, mdprovider.translations['user_name'])