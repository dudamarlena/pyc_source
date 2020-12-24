# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/task/create_task.py
# Compiled at: 2012-10-12 07:02:39
from pytz import timezone
from datetime import datetime, timedelta
from time import time
from coils.core import *
from coils.core.logic import CreateCommand
from keymap import COILS_TASK_KEYMAP
from command import TaskCommand

class CreateTask(CreateCommand, TaskCommand):
    __domain__ = 'task'
    __operation__ = 'new'

    def prepare(self, ctx, **params):
        self.keymap = COILS_TASK_KEYMAP
        self.entity = Task
        CreateCommand.prepare(self, ctx, **params)

    def parse_parameters(self, **params):
        CreateCommand.parse_parameters(self, **params)

    def fill_missing_values(self):
        if self.obj.owner_id is None:
            self.obj.owner_id = self.obj.creator_id
        if self.obj.executor_id is None:
            self.obj.executor_id = self._ctx.account_id
        if self.obj.start is None:
            self.obj.start = datetime.now(tz=timezone('UTC'))
        if self.obj.end is None:
            self.obj.end = self.obj.start + timedelta(days=7)
        if self.obj.notify is None:
            self.obj.notify = 0
        if self.obj.sensitivity is None:
            self.obj.sensitivity = 0
        if self.obj.priority is None:
            self.obj.priority = 0
        if self.obj.complete is None:
            self.obj.complete = 0
        if self.obj.actual is None:
            self.obj.actual = 0
        if self.obj.total is None:
            self.obj.total = 0
        if self.obj.modified is None:
            self.obj.modified
        if self.obj.travel is None:
            self.obj.travel = '0'
        return

    def run(self):
        CreateCommand.run(self)
        self.obj.state = '00_created'
        self.obj.status = 'inserted'
        self.obj.completed = None
        self.obj.creator_id = self._ctx.account_id
        self.fill_missing_values()
        if self.verify_values():
            self.save()
            self._ctx.run_command('task::comment', task=self.obj, values={'comment': self.obj.comment, 'action': '00_created'})
            self.process_attachments()
        else:
            raise CoilsException('Illegal values is task entity.')
        return