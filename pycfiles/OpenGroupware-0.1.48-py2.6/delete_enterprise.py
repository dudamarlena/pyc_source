# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/enterprise/delete_enterprise.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from coils.foundation import *
from coils.logic.address import DeleteCompany

class DeleteEnterprise(DeleteCompany):
    __domain__ = 'enterprise'
    __operation__ = 'delete'

    def __init__(self):
        DeleteCompany.__init__(self)

    def run(self, **params):
        DeleteCompany.run(self, **params)