# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/contact/list.py
# Compiled at: 2012-10-12 07:02:39
import time
from sqlalchemy import *
from coils.core import *
from coils.core.logic import GetCommand

class ListContacts(GetCommand):
    __domain__ = 'contact'
    __operation__ = 'list'

    def parse_parameters(self, **params):
        GetCommand.parse_parameters(self, **params)
        self._props = params.get('properties', [Contact.object_id, Contact.version,
         Contact.first_name, Contact.last_name])
        self._contexts = params.get('contexts', self._ctx.context_ids)
        if isinstance(self._contexts, int):
            self._contexts = [
             self._contexts]
        elif isinstance(self._contexts, basestring):
            self._contexts = [ int(x.strip()) for x in self._contexts.split(',') ]
        elif isinstance(self._contexts, list):
            self._contexts = [ int(x) for x in self._contexts ]
        else:
            raise CoilsException('"contexts" parameter must be an integer, CSV list of integers, or list of integers')
        self._mask = params.get('mask', 'r')
        self._limit = params.get('limit', None)
        return

    def run(self):
        manager = BundleManager.get_access_manager('Contact', self._ctx)
        self._result = manager.List(self._ctx, self._props, contexts=self._contexts, mask=self._mask, limit=self._limit)