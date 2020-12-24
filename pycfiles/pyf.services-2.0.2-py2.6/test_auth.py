# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyf/services/tests/models/test_auth.py
# Compiled at: 2010-05-21 08:57:51
"""Test suite for the TG app's models"""
from nose.tools import eq_
from pyf.services import model
from pyf.services.tests.models import ModelTest

class TestGroup(ModelTest):
    """Unit test case for the ``Group`` model."""
    klass = model.Group
    attrs = dict(group_name='test_group', display_name='Test Group')


class TestUser(ModelTest):
    """Unit test case for the ``User`` model."""
    klass = model.User
    attrs = dict(user_name='ignucius', email_address='ignucius@example.org')

    def test_obj_creation_username(self):
        """The obj constructor must set the user name right"""
        eq_(self.obj.user_name, 'ignucius')

    def test_obj_creation_email(self):
        """The obj constructor must set the email right"""
        eq_(self.obj.email_address, 'ignucius@example.org')

    def test_no_permissions_by_default(self):
        """User objects should have no permission by default."""
        eq_(len(self.obj.permissions), 0)

    def test_getting_by_email(self):
        """Users should be fetcheable by their email addresses"""
        him = model.User.by_email_address('ignucius@example.org')
        eq_(him, self.obj)


class TestPermission(ModelTest):
    """Unit test case for the ``Permission`` model."""
    klass = model.Permission
    attrs = dict(permission_name='test_permission', description='This is a test Description')