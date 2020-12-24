# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/address/create_company.py
# Compiled at: 2012-10-12 07:02:39
from datetime import datetime, timedelta
from pytz import timezone
from sqlalchemy import *
from sqlalchemy.orm import *
from coils.foundation import *
from coils.core import *
from coils.core.logic import CreateCommand
from command import CompanyCommand

class CreateCompany(CreateCommand, CompanyCommand):

    def __init__(self):
        CreateCommand.__init__(self)
        self.sd = ServerDefaultsManager()
        self._C_company_values = {}

    def run(self):
        CreateCommand.run(self)
        self._initialize_addresses()
        self._initialize_company_values()
        self._initialize_telephones()
        self._update_addresses()
        self._update_telephones()
        self._update_company_values()
        self._set_projects()
        self._set_access()
        self.obj.number = ('OGo{0}').format(self.obj.object_id)
        self.obj.login = ('OGo{0}').format(self.obj.object_id)