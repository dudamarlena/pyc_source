# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danjac/petprojects/tesla/tests/output/AuthXpProjectName/authxpprojectname/tests/unit/test_user.py
# Compiled at: 2007-09-06 07:54:22
from authxpprojectname.tests import *

class TestUser(TestModel):

    def setUp(self):
        TestModel.setUp(self)
        self.user = model.User(username='tester', password='test', email='test@here.com')
        self.group = model.Group(name='Subscription Members')
        self.group.permissions.append(model.Permission(name='add_users'))
        model.flush_all()

    def test_authenticate(self):
        assert model.User.authenticate('tester', 'test')
        self.user.password = 'test_again'
        self.user.flush()
        assert model.User.authenticate('tester', 'test_again')

    def test_permissions(self):
        assert not self.user.has_permission('add_users')
        self.group.members.append(self.user)
        model.flush_all()
        self.user.refresh()
        assert self.user.has_permission('add_users')