# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/foundation/get_collection.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *
from coils.core.logic import GetCommand

class GetCollection(GetCommand):
    __domain__ = 'collection'
    __operation__ = 'get'

    def parse_parameters(self, **params):
        GetCommand.parse_parameters(self, **params)
        self._name = params.get('name', None)
        return

    def run(self, **params):
        db = self._ctx.db_session()
        if self._name is not None:
            self.set_single_result_mode()
            query = db.query(Collection).filter(Collection.title == self._name)
        elif self.query_by == 'object_id':
            if len(self.object_ids) > 0:
                query = db.query(Collection).filter(Collection.object_id.in_(self.object_ids))
        else:
            self.set_multiple_result_mode()
            query = db.query(Collection).filter(Collection.owner_id.in_(self._ctx.context_ids))
        self.set_return_value(query.all())
        return