# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/foundation/get_intersection.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *

class GetIntersectingEntities(Command):
    __domain__ = 'collection'
    __operation__ = 'get-intersection'
    mode = None

    def __init__(self):
        Command.__init__(self)

    def parse_parameters(self, **params):
        Command.parse_parameters(self, **params)
        self.collections = params.get('collections', None)
        self.entity_name = params.get('entity_name', None)
        return

    def run(self):
        query_list = []
        db = self._ctx.db_session()
        for collection in self.collections:
            query_list.append(db.query(CollectionAssignment.assigned_id).filter(CollectionAssignment.collection_id == collection.object_id))

        intersect_query = db.execute(intersect(*query_list)).fetchall()
        ids = []
        for id in intersect_query:
            ids.append(id[0])

        if len(ids) > 0:
            result = self._ctx.type_manager.group_ids_by_type(ids)
            if self.entity_name is None:
                self.set_return_value(result)
                return
            self.set_return_value(result.get(self.entity_name, []))
            return
        else:
            self.set_return_value([])
        return