# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/foundation/get_assignments.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *

class GetAssignedEntities(Command):
    __domain__ = 'collection'
    __operation__ = 'get-assignments'
    mode = None

    def __init__(self):
        Command.__init__(self)

    def parse_parameters(self, **params):
        Command.parse_parameters(self, **params)
        self.collection = params.get('collection', None)
        self.entity_name = params.get('entity_name', None)
        self.as_entity = params.get('as_entity', False)
        return

    def run(self):
        db = self._ctx.db_session()
        query = db.query(CollectionAssignment).filter(CollectionAssignment.collection_id == self.collection.object_id)
        query_result = query.all()
        if len(query_result) > 0:
            if self.entity_name is None:
                assignments = query_result
            else:
                assignments = []
                assigned_ids = self._ctx.type_manager.group_ids_by_type([ x.assigned_id for x in query_result ])
                assigned_ids = assigned_ids.get(self.entity_name, [])
                if len(assigned_ids) > 0:
                    for assignment in query_result:
                        if assignment.assigned_id in assigned_ids:
                            assignments.append(assignment)

        else:
            assignments = []
        if self.as_entity:
            entities = self._ctx.type_manager.get_entities([ x.assigned_id for x in assignments ])
            self.set_return_value(entities)
        else:
            self.set_return_value(assignments)
        return