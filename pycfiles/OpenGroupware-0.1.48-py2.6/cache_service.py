# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/contact/cache_service.py
# Compiled at: 2012-10-12 07:02:39
import os, time
from sqlalchemy import and_
from coils.foundation import *
from coils.core import *
from utility import *

class ContactCacheService(Service):
    __service__ = 'coils.contacts.cache'
    __auto_dispatch__ = True
    __is_worker__ = True

    def __init__(self):
        self._cursor = None
        self._iter = 0
        self._next_run = 0.0
        Service.__init__(self)
        return

    def prepare(self):
        Service.prepare(self)
        self._ticktock = time.time()
        self._ctx = AdministrativeContext()

    @property
    def ticktock(self):
        if time.time() - selk._ticktock > 59:
            self._ticktock = time.time()
            return True
        return False

    def _read_data(self):
        self.log.info('Retrieving Contact list for vCard cache fill.')
        query = self._ctx.db_session().query(Contact.object_id, Contact.version).filter(and_(Contact.status != 'archived', Contact.first_name is not None, Contact.last_name is not None)).distinct()
        self._cursor = query.all()
        self._iter = 0
        return

    def work(self):
        if time.time() > self._next_run:
            if self._cursor is None:
                self._read_data()
                self._count = len(self._cursor)
            else:
                if self._iter >= self._count:
                    self.log.info('Refill of vCard cache complete.')
                    self._cursor = None
                    self._next_run = time.time() + 43200.0
                    return
                self.log.debug(('Walking contact cache; items {0}...{1}').format(self._iter, self._iter + 150))
                for i in range(150):
                    if self._iter < self._count:
                        if not is_vcard_cached(self._cursor[self._iter].object_id, self._cursor[self._iter].version):
                            self._ctx.run_command('contact::get-as-vcard', id=self._cursor[self._iter].object_id, access_check=False)
                        self._iter = self._iter + 1
                    else:
                        break

        return