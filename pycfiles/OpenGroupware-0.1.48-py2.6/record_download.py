# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/blob/record_download.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *

class RecordDocumentDownload(Command):
    __domain__ = 'document'
    __operation__ = 'record-download'

    def parse_parameters(self, **params):
        Command.parse_parameters(self, **params)
        if 'document' in params:
            self.object_id = params['document'].object_id
        elif 'id' in params:
            self.object_id = int(params['id'])
        else:
            raise CoilsException('No document specified')

    def run(self, **params):
        db = self._ctx.db_session()
        obj = AuditEntry()
        obj.context_id = self.object_id
        obj.message = 'document downloaded'
        obj.action = 'download'
        obj.actor_id = self._ctx.account_id
        db.add(obj)