# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/enterprise/create_enterprise.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from coils.foundation import *
from coils.logic.address import CreateCompany
from keymap import COILS_ENTERPRISE_KEYMAP
from command import EnterpriseCommand

class CreateEnterprise(CreateCompany, EnterpriseCommand):
    __domain__ = 'enterprise'
    __operation__ = 'new'

    def __init__(self):
        CreateCompany.__init__(self)

    def prepare(self, ctx, **params):
        self.keymap = COILS_ENTERPRISE_KEYMAP
        self.entity = Enterprise
        CreateCompany.prepare(self, ctx, **params)

    def parse_parameters(self, **params):
        CreateCompany.parse_parameters(self, **params)

    def run(self):
        CreateCompany.run(self)
        self.set_contacts()
        self.save()