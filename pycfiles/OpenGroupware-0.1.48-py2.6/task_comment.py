# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/actions/gw/task_comment.py
# Compiled at: 2012-10-12 07:02:39
import os
from pytz import timezone
from datetime import datetime, timedelta
from coils.core import *
from coils.core.logic import ActionCommand
from coils.core.xml import Render as XML_Render

class TaskCommentAction(ActionCommand):
    __domain__ = 'action'
    __operation__ = 'task-comment'
    __aliases__ = ['taskComment', 'taskCommentAction']

    def __init__(self):
        ActionCommand.__init__(self)

    def do_action(self):
        if self._comment is None:
            self._comment = self.rfile.read()
        task = self._ctx.run_command('task::comment', values={'action': 'comment', 'comment': self._comment}, id=self._task_id)
        results = XML_Render.render(task, self._ctx)
        self.wfile.write(results)
        self.wfile.flush()
        return

    def parse_action_parameters(self):
        self._comment = self.action_parameters.get('comment', None)
        if self._comment is not None:
            self._comment = self.process_label_substitutions(self._comment)
        self._task_id = self.action_parameters.get('taskId', self.process.task_id)
        if self._task_id is None:
            raise CoilsException('Attempt to comment on task, but no task available.')
        return