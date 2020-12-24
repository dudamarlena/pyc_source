# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/task/batch_archive.py
# Compiled at: 2012-10-12 07:02:39
import uuid
from datetime import timedelta, datetime
from sqlalchemy import *
from coils.core import *
from command import TaskCommand

class BatchArchive(Command, TaskCommand):
    __domain__ = 'task'
    __operation__ = 'batch-archive'

    def parse_parameters(self, **params):
        Command.parse_parameters(self, **params)
        if 'age' in params:
            self._age = int(params.get('age'))
            self._owner = None
        elif 'owner_id' in params:
            self._owner = int(params.get('owner_id'))
        else:
            raise CoilsException('Neither owner nor age specified for batch archive.')
        fix_completion_dates = params.get('fix_completion_dates', None)
        if fix_completion_dates:
            if isinstance(fix_completion_dates, basestring):
                fix_completion_dates = fix_completion_dates.upper() == 'YES'
            elif isinstance(fix_completion_dates, bool):
                pass
            else:
                fix_completion_dates = False
        else:
            fix_completion_dates = False
        self._fix_completion_date = fix_completion_dates
        return

    def _do_completion_date_fix(self, admin_event_id):
        db = self._ctx.db_session()
        query = db.query(Task).filter(and_(Task.state.in_(['25_done', '02_rejected']), Task.completed is None))
        for task in query.all():
            completed = None
            for action in task.actions:
                if action.action in ('25_done', '02_rejected'):
                    if not completed or action.action_date > completed:
                        completed = action.action_date

            if completed:
                task.completed = completed
                comment = ('Completion date of task corrected to {0}.\nAdministrative event {{{1}}}').format(completed, admin_event_id)
                self._ctx.run_command('task::comment', task=task, values={'comment': comment, 'action': 'archive'})

        return

    def run(self):
        if self._ctx.is_admin:
            admin_event_id = str(uuid.uuid4())
            if self._fix_completion_date:
                self._do_completion_date_fix(admin_event_id)
            counter = 0
            db = self._ctx.db_session()
            comment = ('Auto-archived by administrative event {{{0}}}').format(admin_event_id)
            if self._owner is None:
                now = datetime.now()
                span = timedelta(days=self._age)
                query = db.query(Task).filter(and_(Task.state.in_(['25_done', '02_rejected']), Task.completed is not None, Task.completed < now - span))
            else:
                query = db.query(Task).filter(and_(Task.owner_id == self._owner, Task.state.in_(['25_done', '02_rejected'])))
            for task in query.all():
                self._ctx.run_command('task::comment', task=task, values={'comment': comment, 'action': 'archive'})
                counter += 1

            self._result = counter
        else:
            raise CoilsException('Insufficient privilages to execute task::batch-archive')
        return