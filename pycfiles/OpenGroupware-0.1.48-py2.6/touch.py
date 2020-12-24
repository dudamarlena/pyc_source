# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/token/touch.py
# Compiled at: 2012-10-12 07:02:39
from datetime import datetime
from sqlalchemy import *
from coils.foundation import *
from coils.core import *
from coils.core.logic import *

class TouchToken(GetCommand):
    __domain__ = 'token'
    __operation__ = 'touch'

    def parse_parameters(self, **params):
        Command.parse_parameters(self, **params)
        self._token = params.get('token', None)
        if self._token is None:
            raise CoilsException('No token provided for deletion')
        return

    def run(self, **params):
        self.set_single_result_mode()
        db = self._ctx.db_session()
        if isinstance(self._token, basestring):
            query = db.query(AuthenticationToken).filter(AuthenticationToken.token == self._token)
            self._token = query.first()
        if self._token is not None:
            self._token.touched = self._ctx.get_utctime()
        self.set_return_value([self._token])
        return