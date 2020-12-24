# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/foundation/set_assignments.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *
from keymap import COILS_COLLECTION_ASSIGNMENT_KEYMAP, COILS_COLLECTION_KEYMAP
from command import CollectionAssignmentFlyWeight

class SetAssignments(Command):
    __domain__ = 'collection'
    __operation__ = 'set-assignments'
    mode = None

    def __init__(self):
        Command.__init__(self)

    def parse_parameters(self, **params):
        Command.parse_parameters(self, **params)
        self.collection = params.get('collection', None)
        self.insert = params.get('insert', None)
        self.update = params.get('update', None)
        return

    def check_parameters(self):
        if self.collection is None:
            raise CoilsException('No collection provided to set-assignments')
        return

    def get_max_key(self):
        max_key = 0
        for assignment in self.collection.assignments:
            if assignment.sort_key > max_key:
                max_key = assignment.sort_key

        return max_key

    def delete_assignments_by_id(self, ids):
        db = self._ctx.db_session()
        counter = 0
        query = db.query(CollectionAssignment).filter(and_(CollectionAssignment.collection_id == self.collection.object_id, CollectionAssignment.assigned_id.in_(ids)))
        for x in query.all():
            db.delete(x)
            counter += 1

        return counter

    def get_assignments(self):
        db = self._ctx.db_session()
        query = db.query(CollectionAssignment).filter(CollectionAssignment.collection_id == self.collection.object_id)
        return query.all()

    def get_assigned_ids(self):
        return [ x.assigned_id for x in self.get_assignments() ]

    def _form_assignments(self, assignments):
        if isinstance(assignments, list):
            return [ CollectionAssignmentFlyWeight(assignment, ctx=self._ctx) for assignment in assignments
                   ]
        raise CoilsException('Provided membership must be a list')

    def run(self):
        db = self._ctx.db_session()
        self.check_parameters()
        max_key = self.get_max_key()
        assigned_ids = self.get_assigned_ids()
        if self.insert is not None:
            inserts = self._form_assignments(self.insert)
            counter = 0
            insert_ids = [ x.object_id for x in inserts ]
            for assignment in inserts:
                if assignment.object_id not in assigned_ids:
                    assigned_ids.append(assignment.object_id)
                    counter += 1
                    x = CollectionAssignment()
                    x.collection_id = self.collection.object_id
                    x.assigned_id = assignment.object_id
                    if assignment.sort_key is None:
                        max_key += 1
                        x.sort_key = max_key
                    else:
                        x.sort_key = assignment.sort_key
                    db.add(x)

            self._result = (
             counter, 0, 0)
            return
        else:
            if self.update is not None:
                stats = [
                 0, 0, 0]
                if not isinstance(self.update, list):
                    raise CoilsException(('Update value must be a list, received type "{0}"').format(type(self.update)))
                if len(self.update) == 0:
                    counter = 0
                    for x in self.get_assignments():
                        db.delete(x)
                        stats[2] += 1

                    self._result = stats
                    return
                meta = {}
                for update in self._form_assignments(self.update):
                    meta[update.object_id] = update

                removes = self.get_assigned_ids()
                for x in self.get_assignments():
                    if x.assigned_id in meta:
                        if meta[x.assigned_id].sort_key is not None:
                            x.sort_key = meta[x.assigned_id].sort_key
                        del meta[x.assigned_id]
                        removes.remove(x.assigned_id)
                        stats[1] += 1

                for (assigned_id, assignment) in meta.iteritems():
                    if assignment.__entityName__ is None:
                        kind = self._ctx.type_manager.get_type(assigned_id)
                    else:
                        kind = assignment.__entityName__
                    z = CollectionAssignment()
                    z.collection_id = self.collection.object_id
                    z.assigned_id = assigned_id
                    z.entity_name = kind
                    if assignment.sort_key is not None:
                        z.sort_key = assignment.sort_key
                    else:
                        max_key += 1
                        z.sort_key = max_key
                    db.add(z)
                    stats[0] += 1

                if len(removes) > 0:
                    stats[2] = self.delete_assignments_by_id(removes)
                self._result = stats
                return
            raise CoilsException('No appropriate mode for this collection::set-assignments')
            return