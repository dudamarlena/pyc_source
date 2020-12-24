# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/account/get_defaults.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.foundation import *
from coils.core import *

class GetDefaults(Command):
    __domain__ = 'account'
    __operation__ = 'get-defaults'
    mode = None

    def __init__(self):
        Command.__init__(self)

    def run(self, **params):
        auth_id = self._ctx.account_id
        ud = UserDefaultsManager(auth_id)
        self._result = ud.defaults()