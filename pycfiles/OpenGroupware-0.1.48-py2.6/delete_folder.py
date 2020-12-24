# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/blob/delete_folder.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from coils.core.logic import DeleteCommand
from command import BLOBCommand

class DeleteFolder(DeleteCommand, BLOBCommand):
    __domain__ = 'folder'
    __operation__ = 'delete'

    def prepare(self, ctx, **params):
        DeleteCommand.prepare(self, ctx, **params)

    def get_by_id(self, object_id, access_check):
        return self._ctx.run_command('folder::get', id=object_id, access_check=access_check)

    def run(self):
        db = self._ctx.db_session()
        if self._ctx.is_admin:
            pass
        else:
            rights = self._ctx.access_manager.access_rights(self.obj, contexts=self.context_ids)
            if not ('d' in rights or 'a' in rights):
                raise AccessForbiddenException(('Insufficient privileges to delete {0}').format(self.obj))
        query = db.query(Document).filter(Document.folder_id == self.obj.object_id)
        for document in query.all():
            self._ctx.run_command('document::delete', object=document)

        query = db.query(Folder).filter(Folder.folder_id == self.obj.object_id)
        for folder in query.all():
            self._ctx.run_command('folder::delete', object=folder)

        DeleteCommand.run(self)
        self.notify()