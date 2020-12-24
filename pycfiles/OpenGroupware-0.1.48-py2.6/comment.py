# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/task/comment.py
# Compiled at: 2012-10-12 07:02:39
from pytz import timezone
from time import time
from datetime import datetime
from coils.core import *
from coils.core.logic import CreateCommand
from keymap import COILS_COMMENT_KEYMAP
from command import TaskCommand

class CreateComment(CreateCommand, TaskCommand):
    __domain__ = 'task'
    __operation__ = 'comment'

    def prepare(self, ctx, **params):
        self.keymap = COILS_COMMENT_KEYMAP
        self.entity = TaskAction
        CreateCommand.prepare(self, ctx, **params)

    def parse_parameters(self, **params):
        CreateCommand.parse_parameters(self, **params)
        if 'task' in params:
            self.task = params.get('task')
        elif 'id' in params:
            self.task = self.get_by_id(params.get('id'), self.access_check)
        else:
            raise CoilsException('task parameter required to perform task actions.')

    def audit_action(self):
        log_entry = AuditEntry()
        log_entry.context_id = self.obj.object_id
        log_entry.action = self.action_string
        log_entry.actor_id = self._ctx.account_id
        if self._ctx.login is None:
            log_entry.message = 'Task action performed by anonymous connection'
        else:
            log_entry.message = ('Task action performed by {0}').format(self._ctx.get_login())
        self._ctx.db_session().add(log_entry)
        return

    def do_fix_action(self):
        if self.obj.action is None:
            self.obj.action = '10_commented'
        else:
            self.obj.action = self.obj.action.lower()
            if self.obj.action in ('00_created', '02_rejected', '05_accepted', '10_commented',
                                   '15_divided', '25_done', '27_reactivated', '30_archived'):
                return
            if self.obj.action in 'created':
                self.obj.action = '00_created'
            elif self.obj.action in ('rejected', 'reject'):
                self.obj.action = '02_rejected'
            elif self.obj.action in ('accepted', 'accept'):
                self.obj.action = '05_accepted'
            elif self.obj.action in ('divided', 'divide'):
                self.obj.action = '15_divided'
            elif self.obj.action in ('done', 'completed', 'complete'):
                self.obj.action = '25_done'
            elif self.obj.action in ('activate', 'activated', 'reactivate', 'reactivated'):
                self.obj.action = '27_reactivated'
            elif self.obj.action in ('archived', 'archive'):
                self.obj.action = '30_archived'
            else:
                self.obj.action = '10_commented'
        return

    def do_perform_action(self):
        if self.obj.action == '00_created':
            return
        else:
            if self.obj.action == '02_rejected':
                if self.task.state not in ('20_done', '30_archived'):
                    self.task.state = '02_rejected'
            elif self.obj.action == '05_accepted':
                if self.task.state == '00_created':
                    self.task.state = '20_processing'
                    self.task.executor_id = self._ctx.account_id
            elif self.obj.action == '15_divided':
                self.obj.action = '10_commented'
            elif self.obj.action == '25_done':
                if self.task.state != '30_archived':
                    self.task.state = '25_done'
                    self.task.completed = datetime.now(tz=timezone('UTC'))
            elif self.obj.action == '27_reactivated':
                self.task.state = '00_created'
                self.task.completed = None
            elif self.obj.action == '30_archived':
                self.task.state = '30_archived'
            return

    def run(self):
        CreateCommand.run(self)
        self.obj.task_id = self.task.object_id
        self.obj.actor_id = self._ctx.account_id
        self.do_fix_action()
        self.action_string = self.obj.action
        if self.obj.comment is None:
            self.obj.comment = ''
        if self.action_string is None:
            raise CoilsException('Request to perform a NULL action')
        self.do_perform_action()
        self.obj.action_date = datetime.now(tz=timezone('UTC'))
        self.obj.task_status = self.task.state
        self.obj.status = 'inserted'
        self.save()
        self.obj = self.task
        if self.obj.version is None:
            self.obj.version = 2
        else:
            self.obj.version += 1
        self.obj.status = 'updated'
        self._result = self.obj
        return