# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/task/update_task.py
# Compiled at: 2012-10-12 07:02:39
from pytz import timezone
from time import time
from coils.core import *
from coils.core.logic import UpdateCommand
from keymap import COILS_TASK_KEYMAP
from command import TaskCommand

class UpdateTask(UpdateCommand, TaskCommand):
    __domain__ = 'task'
    __operation__ = 'set'

    def prepare(self, ctx, **params):
        self.keymap = COILS_TASK_KEYMAP
        UpdateCommand.prepare(self, ctx, **params)

    def run(self):
        UpdateCommand.run(self)
        self.process_attachments()
        self.obj.status = 'updated'
        if not self.verify_values():
            raise CoilsException('Illegal values is task entity.')