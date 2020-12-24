# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/summermvc/templates/project_demo/src/dao/user_dao.py
# Compiled at: 2018-05-30 05:31:20
from summermvc.decorator import *
from summermvc.field import *

@repository
class UserDao(object):
    configuration = AutoWiredField('DBConfiguration')

    @post_construct
    def setup(self):
        print 'user dao is constructed'
        print (
         'configuration is:', self.configuration)

    @pre_destroy
    def teardown(self):
        print 'user dao is destroyed'

    def get_user_by_id(self, user_id):
        print 'UserDao.get_user_by_id(%s)' % user_id
        return {'user_id': user_id, 'name': 'Tim Chow'}