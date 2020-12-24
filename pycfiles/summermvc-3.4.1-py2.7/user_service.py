# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/summermvc/templates/project_demo/src/service/user_service.py
# Compiled at: 2018-05-30 05:31:20
from summermvc.decorator import *

@service
class UserService(object):

    @post_construct
    def setup(self):
        print 'user service is constructed'

    @auto_wired
    def _user_dao(self):
        pass

    def get_user_by_id(self, user_id):
        print 'UserService.get_user_by_id(%s)' % user_id
        data = self._user_dao.get_user_by_id(user_id)
        print ('data is:', data)
        return data