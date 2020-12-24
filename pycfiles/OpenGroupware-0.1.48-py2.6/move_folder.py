# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/blob/move_folder.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from coils.foundation import *
from command import BLOBCommand

class MoveFolder(SetCommand, BLOBCommand):
    __domain__ = 'folder'
    __operation__ = 'move'

    def __init__(self):
        Command.__init__(self)

    def parse_parameters(self, **params):
        SetCommand.parse_parameters(self, **params)
        self.obj = params.get('folder', None)
        self.filename = params.get('to_filename', None)
        self.to_folder = params.get('to_folder', None)
        return

    def get_by_id(self, object_id, access_check):
        return self._ctx.run_command('folder::get', id=object_id, access_check=access_check)

    def run(self):
        if self.access_check:
            rights = self._ctx.access_manager.access_rights(self.obj, contexts=self.context_ids)
            print ('RIGHTS: {0}').format(rights)
            if self.debug:
                self.log.debug(('Rights found for documentId#{0} entity: {1}').format(self.obj.object_id, rights))
            if 'w' not in rights:
                raise AccessForbiddenException(('Insufficient privileges to modify documentId#{0}').format(self.obj.object_id))
        if self.to_folder:
            self.to_folder.modified = self._ctx.get_utctime()
            self.to_folder.status = 'updated'
            if self.obj.folder_id != self.to_folder.object_id:
                if self.obj.project_id != self.to_folder.project_id:
                    raise NotImplementedException('Folders cannot be moved between projects')
                if self.access_check:
                    rights = self._ctx.access_manager.access_rights(self.to_folder, contexts=self.context_ids)
                    if self.debug:
                        self.log.debug(('Rights found for folderId#{0} entity: {1}').format(self.to_folder.object_id, rights))
                    if 'w' not in rights:
                        raise AccessForbiddenException(('Insufficient privileges to place documentId#{0} into folderId#{1}').format(self.obj.object_id, self.to_folder.object_id))
                self.obj.folder_id = self.to_folder.object_id
                if self.to_folder.version:
                    self.to_folder.version += 1
                else:
                    self.to_folder.version = 2
        if self.filename:
            self.obj.name = self.filename
        self.increment_version()
        self.set_result(self.obj)