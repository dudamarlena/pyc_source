# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/enterprise/search_enterprise.py
# Compiled at: 2012-10-12 07:02:39
from datetime import datetime, timedelta
from pytz import timezone
from sqlalchemy import *
from sqlalchemy.orm import *
from coils.foundation import *
from coils.core import *
from coils.logic.address import SearchCompany
from keymap import COILS_ENTERPRISE_KEYMAP

class SearchEnterprise(SearchCompany):
    __domain__ = 'enterprise'
    __operation__ = 'search'
    mode = None

    def __init__(self):
        SearchCompany.__init__(self)

    def prepare(self, ctx, **params):
        SearchCompany.prepare(self, ctx, **params)

    def parse_parameters(self, **params):
        SearchCompany.parse_parameters(self, **params)

    def add_result(self, contact):
        if enterprise not in self._result:
            self._result.append(enterprise)

    def do_revolve(self):
        contacts = []
        for enterprise in self._result:
            for assignment in enterprise.contacts:
                if int(assignment.child_id) not in contacts:
                    contacts.append(int(assignment.child_id))

        return self._ctx.run_command('contact::get', ids=contacts)

    def run(self):
        self._query = self._parse_criteria(self._criteria, Enterprise, COILS_ENTERPRISE_KEYMAP)
        data = self._query.all()
        self.log.debug('query returned %d objects' % len(data))
        self.set_return_value(data)