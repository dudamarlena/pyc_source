# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/delete_process.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from coils.foundation import *
from coils.core.logic import DeleteCommand
from utility import *

class DeleteProcess(DeleteCommand):
    __domain__ = 'process'
    __operation__ = 'delete'

    def get_by_id(self, pid, access_check):
        return self._ctx.run_command('process::get', id=pid, access_check=access_check)

    def run(self):
        self.log.debug(('Deleting data for processId#{0}').format(self.obj.object_id))
        BLOBManager.DeleteShelf(uuid=self.obj.uuid)
        messages = self._ctx.run_command('process::get-messages', process=self.obj)
        for message in messages:
            self.log.debug(('Deleting message {0}').format(message.uuid))
            self._ctx.run_command('message::delete', uuid=message.uuid)

        for vid in range(self.obj.version):
            BLOBManager.Delete(filename_for_versioned_process_code(self.obj.object_id, vid))

        for filename in [filename_for_process_markup(self.obj), filename_for_process_code(self.obj)]:
            BLOBManager.Delete(filename)

        DeleteCommand.run(self)