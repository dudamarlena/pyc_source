# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/foundation/assign_object.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *
from keymap import COILS_COLLECTION_ASSIGNMENT_KEYMAP

class AssignObject(Command):
    __domain__ = 'object'
    __operation__ = 'assign-to-collection'
    mode = None

    def __init__(self):
        Command.__init__(self)

    def parse_parameters(self, **params):
        Command.parse_parameters(self, **params)
        self.collection = params.get('collection', None)
        self.assigned = params.get('entity', None)
        return

    def check_parameters(self):
        if self.collection is None:
            raise CoilsException('No collection provided to set-assignment')
        return

    def get_max_key(self):
        max_key = 0
        for assignment in self.collection.assignments:
            if assignment.sort_key > max_key:
                max_key = assignment.sort_key

        return max_key

    def get_assignment(self):
        db = self._ctx.db_session()
        query = db.query(CollectionAssignment).filter(and_(CollectionAssignment.collection_id == self.collection.object_id, CollectionAssignment.assigned_id == self.assigned.object_id))
        result = query.all()
        if result:
            return result[0]
        else:
            return
            return

    def run(self):
        db = self._ctx.db_session()
        self.check_parameters()
        self.obj = self.get_assignment()
        if not self.obj:
            self.obj = CollectionAssignment()
            self.obj.collection_id = self.collection.object_id
            self.obj.assigned_id = self.assigned.object_id
            self.obj.sort_key = self.get_max_key()
            self._ctx.db_session().add(self.obj)
            self.collection.version += 1
        self.set_return_value(self.collection)