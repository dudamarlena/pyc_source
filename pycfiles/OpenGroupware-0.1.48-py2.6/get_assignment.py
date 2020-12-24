# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/foundation/get_assignment.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *

class GetAssignment(Command):
    __domain__ = 'collection'
    __operation__ = 'get-assignment'
    mode = None

    def __init__(self):
        Command.__init__(self)

    def parse_parameters(self, **params):
        Command.parse_parameters(self, **params)
        if 'id' in params:
            self._assignment_ids = [int(params.get('id'))]
        elif 'ids' in params:
            self._assignment_ids = [ int(x) for x in params.get('ids') ]
        else:
            raise CoilsException('No assignments specified for retrieval')

    def get_targets(self, target_ids):
        result = {}
        assigned_ids = self._ctx.type_manager.group_ids_by_type(target_ids)
        if 'Contact' in assigned_ids:
            for entity in self._ctx.run_command('contact::get', ids=assigned_ids['Contact']):
                result[entity.object_id] = entity

        if 'Project' in assigned_ids:
            for entity in self._ctx.run_command('project::get', ids=assigned_ids['Project']):
                result[entity.object_id] = entity

        if 'Task' in assigned_ids:
            for entity in self._ctx.run_command('task::get', ids=assigned_ids['Task']):
                result[entity.object_id] = entity

        if 'Document' in assigned_ids:
            for entity in self._ctx.run_command('document::get', ids=assigned_ids['Document']):
                result[entity.object_id] = entity

        if 'Folder' in assigned_ids:
            for entity in self._ctx.run_command('folder::get', ids=assigned_ids['Folder']):
                result[entity.object_id] = entity

        return result

    def get_collections(self, collection_ids):
        result = {}
        for collection in self._ctx.run_command('collection::get', ids=collection_ids):
            result[collection.object_id] = collection

        return result

    def run(self):
        db = self._ctx.db_session()
        query = db.query(CollectionAssignment).filter(CollectionAssignment.object_id.in_(self._assignment_ids))
        query_result = query.all()
        collections = self.get_collections(set([ assignment.collection_id for assignment in query_result ]))
        targets = self.get_targets([ assignment.assigned_id for assignment in query_result ])
        result = {}
        for entry in query_result:
            result[entry.object_id] = (
             collections.get(entry.collection_id, None), targets.get(entry.assigned_id, None))

        self.set_return_value(result)
        return