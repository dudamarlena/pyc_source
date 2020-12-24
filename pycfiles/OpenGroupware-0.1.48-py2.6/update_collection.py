# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/foundation/update_collection.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from coils.core.logic import UpdateCommand
from keymap import COILS_COLLECTION_KEYMAP
from command import CollectionAssignmentFlyWeight

class UpdateCollection(UpdateCommand):
    __domain__ = 'collection'
    __operation__ = 'set'

    def __init__(self):
        UpdateCommand.__init__(self)

    def prepare(self, ctx, **params):
        self.keymap = COILS_COLLECTION_KEYMAP
        self.entity = Collection
        UpdateCommand.prepare(self, ctx, **params)

    def parse_parameters(self, **params):
        UpdateCommand.parse_parameters(self, **params)

    def _form_assignments(self, assignments):
        if isinstance(assignments, list):
            return [ CollectionAssignmentFlyWeight(assignment, ctx=self._ctx) for assignment in assignments
                   ]
        raise CoilsException('Provided membership must be a list')

    def do_assignments(self):
        membership = KVC.subvalues_for_key(self.values, ['_MEMBERSHIP', 'membership'])
        assignments = self._form_assignments(membership)
        if len(assignments) > 0:
            self._ctx.run_command('collection::set-assignments', update=assignments, collection=self.obj)

    def get_by_id(self, object_id, access_check):
        return self._ctx.run_command('collection::get', id=object_id, access_check=access_check)

    def run(self):
        UpdateCommand.run(self)
        self.do_assignments()