# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/project/delete_project.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from coils.core.logic import DeleteCommand
from command import ProjectCommand

class DeleteProject(DeleteCommand, ProjectCommand):
    __domain__ = 'project'
    __operation__ = 'delete'

    def prepare(self, ctx, **params):
        DeleteCommand.prepare(self, ctx, **params)

    def parse_parameters(self, **params):
        DeleteCommand.parse_parameters(self, **params)

    def get_by_id(self, object_id, access_check):
        return self._ctx.run_command('project::get', id=object_id, access_check=access_check)

    def run(self):
        if self._ctx.is_admin:
            pass
        else:
            rights = self._ctx.access_manager.access_rights(self.obj, contexts=self.context_ids)
            if not ('d' in rights or 'a' in rights):
                raise AccessForbiddenException(('Insufficient privileges to delete {0}').format(self.obj))
        notes = self._ctx.run_command('project::get-notes', project=self.obj)
        for note in notes:
            note.project_id = None

        self.purge_assignments()
        folder = self._ctx.run_command('project::get-root-folder', project=self.obj)
        if folder:
            self._ctx.run_command('folder::delete', object=folder)
        DeleteCommand.run(self)
        self.notify()
        return