# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/actions/gw/archive_old_tasks.py
# Compiled at: 2012-10-12 07:02:39
from lxml import etree
from coils.core import *
from coils.core.logic import ActionCommand

class ArchiveOldTasksAction(ActionCommand):
    __domain__ = 'action'
    __operation__ = 'archive-old-tasks'
    __aliases__ = ['archiveOldTasks', 'archiveOldTasksAction']

    def __init__(self):
        ActionCommand.__init__(self)

    def do_action(self):
        if self._ctx.is_admin:
            result = self._ctx.run_command('task::batch-archive', age=self._age_days)
            self.wfile.write(unicode(result))
        else:
            raise CoilsException('Insufficient privilages to invoke archiveAccountTasksAction')

    def parse_action_parameters(self):
        self._age_days = self.action_parameters.get('days', 187)
        if self._age_days is not None:
            self._age_days = int(self.process_label_substitutions(self._age_days))
        return