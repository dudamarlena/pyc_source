# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/enterprise/get_companyvalue.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *
from command import EnterpriseCommand

class GetCompanyValue(Command, EnterpriseCommand):
    __domain__ = 'enterprise'
    __operation__ = 'get-companyvalue'
    mode = None

    def __init__(self):
        self.access_check = True
        Command.__init__(self)

    def parse_parameters(self, **params):
        Command.parse_parameters(self, **params)
        self._enterprise = params.get('enterprise', None)
        self._name = params.get('name', None)
        return

    def run(self):
        self.access_check = False
        db = self._ctx.db_session()
        query = db.query(CompanyValue).filter(and_(CompanyValue.parent_id == self._enterprise.object_id, CompanyValue.name == self._name))
        result = query.all()
        if result:
            self.set_return_value(result[0])
        else:
            self.set_return_value(None)
        return