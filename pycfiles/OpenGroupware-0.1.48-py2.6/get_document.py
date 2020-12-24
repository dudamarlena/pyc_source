# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/blob/get_document.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *
from coils.core.logic import GetCommand

class GetDocument(GetCommand):
    __domain__ = 'document'
    __operation__ = 'get'

    def run(self, **params):
        db = self._ctx.db_session()
        query = db.query(Document).filter(Document.object_id.in_(self.object_ids))
        self.set_return_value(query.all())