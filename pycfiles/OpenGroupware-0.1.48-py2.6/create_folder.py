# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/blob/create_folder.py
# Compiled at: 2012-10-12 07:02:39
from coils.foundation import *
from coils.core import *
from coils.core.logic import CreateCommand
from command import BLOBCommand
from keymap import COILS_FOLDER_KEYMAP

class CreateFolder(CreateCommand, BLOBCommand):
    __domain__ = 'folder'
    __operation__ = 'new'

    def prepare(self, ctx, **params):
        self.keymap = COILS_FOLDER_KEYMAP
        self.entity = Folder
        CreateCommand.prepare(self, ctx, **params)

    def parse_parameters(self, **params):
        CreateCommand.parse_parameters(self, **params)
        self._parent = params.get('folder', None)
        return

    def run(self):
        CreateCommand.run(self)
        self.obj.owner_id = self._ctx.account_id
        self.obj.creator_id = self._ctx.account_id
        if not self._parent:
            if self.obj.folder_id:
                self._parent = self._ctx.run_command('folder::get', id=self.obj.folder_id)
                if not self._parent:
                    raise CoilsException(('Cannot marshal parent folderId#{0}').format(self.object.folder_id))
        else:
            self.obj.folder_id = self._parent.object_id
        if self._parent:
            self.obj.project_id = self._parent.project_id
        self.inherit_acls()
        self.save()
        self._ctx.flush()