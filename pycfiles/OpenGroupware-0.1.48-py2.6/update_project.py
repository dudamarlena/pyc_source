# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/project/update_project.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *
from coils.core.logic import UpdateCommand
from keymap import COILS_PROJECT_KEYMAP

class UpdateProject(UpdateCommand):
    __domain__ = 'project'
    __operation__ = 'set'

    def prepare(self, ctx, **params):
        self.keymap = COILS_PROJECT_KEYMAP
        UpdateCommand.prepare(self, ctx, **params)

    def get_by_id(self, object_id, access_check):
        return self._ctx.run_command('project::get', id=object_id, contexts=self.context_ids, access_check=access_check)

    def run(self):
        UpdateCommand.run(self)
        self.obj.status = 'updated'
        self.notify()