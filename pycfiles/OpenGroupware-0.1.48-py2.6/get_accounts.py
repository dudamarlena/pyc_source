# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/account/get_accounts.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *
from coils.core.logic import GetCommand
from coils.foundation import Project, Appointment, Contact, Enterprise

class GetAccounts(GetCommand):
    __domain__ = 'account'
    __operation__ = 'get-all'

    def run(self, **params):
        db = self._ctx.db_session()
        self.access_check = False
        self.mode = 2
        query = db.query(Contact).filter(Contact.is_account == 1)
        self.set_return_value(query.all())