# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/foundation/delete_assignment.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *

class DeleteCollectionAssignment(Command):
    __domain__ = 'collection'
    __operation__ = 'delete-assignment'

    def parse_parameters(self, **params):
        Command.parse_parameters(self, **params)
        self.collection = params.get('collection', None)
        if 'entity' in params:
            self.assigned_id = params.get('entity').object_id
        elif 'assigned_id' in params:
            self.assigned_id = int(params.get('assigned_id'))
        else:
            raise CoilException('Assignment to delete not specified as entity or assigned_id')
        return

    def run(self):
        self.collection.version += 1
        self._ctx.db_session().query(CollectionAssignment).filter(and_(CollectionAssignment.collection_id == self.collection.object_id, CollectionAssignment.assigned_id == self.assigned_id)).delete(synchronize_session='fetch')
        self.set_return_value(True)