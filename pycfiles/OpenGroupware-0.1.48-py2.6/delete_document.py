# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/blob/delete_document.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from coils.foundation import *
from coils.core.logic import DeleteCommand
from command import BLOBCommand

class DeleteDocument(DeleteCommand, BLOBCommand):
    __domain__ = 'document'
    __operation__ = 'delete'

    def __init__(self):
        DeleteCommand.__init__(self)
        self._common_init()

    def get_by_id(self, object_id, access_check):
        return self._ctx.run_command('document::get', id=object_id, access_check=access_check)

    def run(self):
        if self.access_check:
            if self._ctx.is_admin:
                pass
            else:
                rights = self._ctx.access_manager.access_rights(self.obj, contexts=self.context_ids)
                if self.debug:
                    self.log.debug(('Rights found for documentId#{0} entity: {1}').format(self.obj.object_id, rights))
                if 'd' not in rights:
                    raise AccessForbiddenException(('Insufficient privileges to delete documentId#{0}').format(self.obj.object_id))
        self.set_result(False)
        manager = self.get_manager(self.obj)
        document_path = manager.get_path(self.obj)
        versions = self._ctx.run_command('document::get-versions', document=self.obj)
        paths = [document_path]
        for version in range(0, self.obj.version_count + 1):
            version_path = manager.get_path(self.obj, version=version)
            if version_path:
                paths.append(version_path)

        for path in paths:
            if self.debug:
                self.log.debug(('Deleting document path "{0}".').format(path))
            BLOBManager.Delete(path)

        if self.debug:
            self.log.debug(('Deleting database entities for documentId#{0}').format(self.obj.object_id))
        DeleteCommand.run(self)
        self.set_result(True)