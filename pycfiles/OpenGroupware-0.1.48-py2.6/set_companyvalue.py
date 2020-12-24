# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/enterprise/set_companyvalue.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *
from command import EnterpriseCommand

class SetCompanyValue(Command, EnterpriseCommand):
    __domain__ = 'enterprise'
    __operation__ = 'set-companyvalue'
    mode = None

    def __init__(self):
        self.access_check = True
        Command.__init__(self)

    def parse_parameters(self, **params):
        Command.parse_parameters(self, **params)
        self._enterprise = params.get('enterprise', None)
        self._name = params.get('name', None)
        self._value = params.get('value', None)
        return

    def run(self):
        if not self._name:
            raise CoilsException('No attribute name specified')
        cv = self._ctx.run_command('enterprise::get-companyvalue', enterprise=self._enterprise, name=self._name)
        if cv:
            cv.set_value(self._value)
        else:
            cv = CompanyValue(self._contact.object_id, self._name, self._value)
            self._ctx.db_session().add(cv)
        self.set_return_value(cv)