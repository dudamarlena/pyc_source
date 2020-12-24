# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/summermvc/templates/project_demo/src/aspect/user_dao_aspect.py
# Compiled at: 2018-05-30 05:31:20
from summermvc.decorator import *
from summermvc import return_value

@component
@aspect(1)
class UserDaoAspect(object):

    @around('UserDao get_.*')
    def get_aspect(self, joint_point):
        print 'get_aspect() is invoked.'
        result = yield
        print 'result is: %s' % result
        print 'get_aspect() is invoked.'