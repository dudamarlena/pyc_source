# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/bigdoorkit/resources/user.py
# Compiled at: 2010-07-29 15:08:39
from bigdoorkit.resources.base import BDResource

class EndUser(BDResource):
    endpoint = 'end_user'

    def __init__(self, **kw):
        self.guid = guid
        self.end_user_login = kw.get('end_user_login', None)
        super(EndUser, self).__init__(**kw)
        return