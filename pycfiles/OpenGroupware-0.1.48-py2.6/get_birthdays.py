# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/contact/get_birthdays.py
# Compiled at: 2012-10-12 07:02:39
from datetime import datetime
from sqlalchemy import *
import sqlalchemy.sql as sql
from coils.core import *
from coils.logic.address import GetCompany

class GetUpcomingBirthdays(GetCompany):
    __domain__ = 'contact'
    __operation__ = 'get-upcoming-birthdays'
    mode = None

    def __init__(self):
        self.access_check = True
        GetCompany.__init__(self)

    def parse_parameters(self, **params):
        GetCompany.parse_parameters(self, **params)
        self.accounts = 0
        if 'accounts' in params:
            if params.get('accounts'):
                self.accounts = 1

    def run(self):
        db = self._ctx.db_session()
        doy = datetime.today().timetuple().tm_yday
        floor = doy - 2
        if floor < 1:
            floor += 365
        ceiling = doy + 14
        if ceiling > 365:
            ceiling -= 365
        orm_doy = sql.expression.extract('doy', Contact.birth_date)
        query = db.query(Contact).filter(and_(sql.expression.between(orm_doy, floor, ceiling), Contact.birth_date != None, Contact.is_account == self.accounts, Contact.status != 'archived'))
        self.set_multiple_result_mode()
        self.set_return_value(query.all())
        return