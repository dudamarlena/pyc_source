# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/foundation/delete_note.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from coils.foundation import *
from coils.core.logic import DeleteCommand

class DeleteNote(DeleteCommand):
    __domain__ = 'note'
    __operation__ = 'delete'

    def __init__(self):
        DeleteCommand.__init__(self)

    def get_by_id(self, object_id, access_check):
        return self._ctx.run_command('note::get', id=object_id, access_check=access_check)

    def run(self):
        BLOBManager.Delete(self.obj.get_path())
        DeleteCommand.run(self)