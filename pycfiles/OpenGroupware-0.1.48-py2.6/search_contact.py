# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/contact/search_contact.py
# Compiled at: 2012-10-12 07:02:39
from datetime import datetime, timedelta
from pytz import timezone
from sqlalchemy import *
from sqlalchemy.orm import *
from coils.foundation import *
from coils.core import *
from coils.logic.address import SearchCompany
from keymap import COILS_CONTACT_KEYMAP

class SearchContacts(SearchCompany):
    __domain__ = 'contact'
    __operation__ = 'search'
    mode = None

    def __init__(self):
        SearchCompany.__init__(self)

    def prepare(self, ctx, **params):
        SearchCompany.prepare(self, ctx, **params)

    def parse_parameters(self, **params):
        SearchCommand.parse_parameters(self, **params)

    def add_result(self, contact):
        if contact not in self._result:
            self._result.append(contact)

    def do_revolve(self):
        enterprises = []
        for contact in self._result:
            for assignment in contact.enterprises:
                if int(assignment.parent_id) not in enterprises:
                    enterprises.append(int(assignment.parent_id))

        return self._ctx.run_command('enterprise::get', ids=enterprises)

    def run(self):
        self._query = self._parse_criteria(self._criteria, Contact, COILS_CONTACT_KEYMAP)
        import time
        start = time.time()
        data = self._query.all()
        print '----'
        print time.time() - start
        self.log.debug('query returned %d objects' % len(data))
        self.set_return_value(data)