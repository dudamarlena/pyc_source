# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/registration/ormmanager/tests/testsa.py
# Compiled at: 2008-07-04 10:34:30
from registration.ormmanager.tests.samodel import User, Group, users_table, groups_table, user_group_table, metadata
from registration.ormmanager.tests.generic import GeneralTests, set_user_class
from turbogears.database import session
from registration import ormmanager
from somodel import hub, __connection__

class TestSqlAlchemy(GeneralTests):

    def __init__(self):
        super(TestSqlAlchemy, self).__init__()
        set_user_class(User)

    def setUp(self):
        metadata.drop_all()
        metadata.create_all()
        user1 = User()
        user1.user_name = 'bobvilla'
        user1.email_address = 'bob@homedepot.com'
        user1.display_name = 'Bob Villa'
        user1.password = 'toughasnails'
        session.save(user1)
        u2 = User()
        u2.user_name = 'bobathome'
        u2.email_address = 'bob@home.com'
        u2.display_name = 'Bob Villa'
        u2.password = 'hammertime'
        session.save(u2)
        session.flush()
        print 'UuUuUuU %s' % user1
        self.user1 = user1
        session.clear()
        session.close()

    def tearDown(self):
        metadata.drop_all()

    def test_create(self):
        """Create a new object."""
        u = ormmanager.create(User, user_name='bobevans', email_address='bob@example.com', display_name='Bob Evans', password='secretsauce')
        assert u.user_name == 'bobevans'
        assert u.user_id > 0

    def test_setup(self):
        """Make sure our setup is what we think it is."""
        u1 = session.query(User).filter_by(user_name='bobvilla')
        l = session.query(User).all()
        print u1
        for u in l:
            print u

        assert u1[0].user_id == self.user1.user_id
        assert u1[0].email_address == 'bob@homedepot.com'
        assert len(l) == 2