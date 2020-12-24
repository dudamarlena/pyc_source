# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/account/get_account.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *
from coils.core.logic import GetCommand, RETRIEVAL_MODE_SINGLE, RETRIEVAL_MODE_MULTIPLE

class GetAccount(GetCommand):
    __domain__ = 'account'
    __operation__ = 'get'

    def parse_parameters(self, **params):
        GetCommand.parse_parameters(self, **params)
        self._login = None
        if 'login' in params:
            self._login = params.get('login')
        return

    def run(self, **params):
        db = self._ctx.db_session()
        if self._login is not None:
            self.mode = RETRIEVAL_MODE_SINGLE
            self.log.debug(('attempting to retrieve contact object with login of "{0}"').format(self._login))
            query = db.query(Contact).filter(and_(Contact.login == self._login, Contact.is_account == 1, Contact.status != 'archived'))
        else:
            if len(self.object_ids) == 0:
                self.mode = RETRIEVAL_MODE_SINGLE
                self.object_ids.append(self._ctx.account_id)
            query = db.query(Contact).filter(and_(Contact.object_id.in_(self.object_ids), Contact.is_account == 1, Contact.status != 'archived'))
        self.set_return_value(query.all())
        return