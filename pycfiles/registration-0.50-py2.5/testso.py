# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/registration/ormmanager/tests/testso.py
# Compiled at: 2008-07-04 10:34:30
from registration.ormmanager.tests.somodel import User, Group
from registration.ormmanager.tests.generic import GeneralTests, set_user_class

class TestSqlObject(GeneralTests):

    def __init__(self):
        super(TestSqlObject, self).__init__()
        set_user_class(User)

    def setUp(self):
        User.createTable()
        Group.createTable()
        self.user1 = User(user_name='bobvilla', email_address='bob@homedepot.com', display_name='Bob Villa', password='toughasnails')
        u2 = User(user_name='bobathome', email_address='bob@home.com', display_name='Bob Villa', password='hammertime')

    def test_setup(self):
        """Ensure our setup has been processed."""
        assert User.tableExists()
        u2 = User.selectBy(email_address='bob@home.com')[0]
        print u2
        assert u2.user_name == 'bobathome'

    def tearDown(self):
        User.dropTable()
        Group.dropTable()