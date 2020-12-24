# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/actions/gw/task_create.py
# Compiled at: 2012-10-12 07:02:39
from pytz import timezone
from datetime import datetime, timedelta
from coils.core import *
from coils.core.logic import ActionCommand
from coils.core.xml import Render as XML_Render

class CreateTaskAction(ActionCommand):
    __domain__ = 'action'
    __operation__ = 'create-task'
    __aliases__ = ['createTask', 'createTaskAction']

    def __init__(self):
        ActionCommand.__init__(self)

    def do_action(self):
        task = self._ctx.run_command('task::new', values=self._values)
        if task is None:
            raise CoilsException('Failed to create entity.')
        if self._tiein:
            self.process.task_id = task.object_id
        results = XML_Render.render(task, self._ctx)
        self.wfile.write(results)
        self.wfile.flush()
        return

    def _get_attribute_from_params(self, name, default=None):
        x = unicode(self.action_parameters.get(name, default))
        return unicode(self.process_label_substitutions(x))

    def parse_action_parameters(self):
        self._values = {'comment': self._get_attribute_from_params('comment', ''), 
           'name': self._get_attribute_from_params('name', ''), 
           'start': self._get_attribute_from_params('start', ''), 
           'kind': self._get_attribute_from_params('kind'), 
           'sensitivity': self._get_attribute_from_params('sensitivity', '0'), 
           'priority': self._get_attribute_from_params('priority', '3'), 
           'executorid': self._get_attribute_from_params('executor', self._ctx.account_id), 
           'ownerid': self._get_attribute_from_params('owner', self._ctx.account_id)}
        if 'start' not in self.action_parameters:
            self._values['start'] = datetime.now()
        else:
            self._values['start'] = datetime(int(self._values['start'][0:4]), int(self._values['start'][5:7]), int(self._values['start'][8:10]), tzinfo=timezone('UTC'))
        if 'duration' in self.action_parameters:
            self._values['end'] += self._values['start'] + timedelta(days=int(self.action_parameters.get('duration')))
        elif 'end' in self.action_parameters:
            self._values['end'] = self.process_label_substitutions(self.action_parameters.get('end'))
        if 'project' in self.action_parameters:
            project_id = self._get_attribute_from_params('project', default=0)
            try:
                project_id = int(project_id)
            except:
                project_id = None
            else:
                if project_id < 10003:
                    project_id = None

            self._values['project_id'] = project_id
        if 'parent' in self.action_parameters:
            parent_id = self._get_attribute_from_params('parent', default=0)
            try:
                parent_id = int(parent_id)
            except:
                parent_id = None
            else:
                if parent_id < 10003:
                    parent_id = None

            self._values['parent_id'] = parent_id
        if self.action_parameters.get('workflowTask', 'YES').upper() == 'YES':
            self._tiein = True
        else:
            self._tiein = False
        return