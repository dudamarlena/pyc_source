# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/address/update_company.py
# Compiled at: 2012-10-12 07:02:39
import pprint
from sqlalchemy import *
from coils.core import *
from coils.core.logic import UpdateCommand
from command import CompanyCommand

class UpdateCompany(UpdateCommand, CompanyCommand):

    def __init__(self):
        UpdateCommand.__init__(self)
        self.sd = ServerDefaultsManager()
        self._C_company_values = {}

    def parse_parameters(self, **params):
        UpdateCommand.parse_parameters(self, **params)

    def run(self):
        UpdateCommand.run(self)
        self._update_telephones()
        self._update_addresses()
        self._update_company_values()
        self._set_projects()
        self._set_access()