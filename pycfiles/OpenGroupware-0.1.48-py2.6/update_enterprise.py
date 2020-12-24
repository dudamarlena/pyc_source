# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/enterprise/update_enterprise.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from coils.logic.address import UpdateCompany
from command import EnterpriseCommand
from keymap import COILS_ENTERPRISE_KEYMAP

class UpdateEnterprise(UpdateCompany, EnterpriseCommand):
    __domain__ = 'enterprise'
    __operation__ = 'set'

    def prepare(self, ctx, **params):
        self.keymap = COILS_ENTERPRISE_KEYMAP
        UpdateCompany.prepare(self, ctx, **params)

    def get_by_id(self, object_id, access_check):
        return self._ctx.run_command('enterprise::get', id=object_id, access_check=access_check)

    def prepare(self, ctx, **params):
        self.keymap = COILS_ENTERPRISE_KEYMAP
        UpdateCompany.prepare(self, ctx, **params)
        self.set_contacts()