# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/task/get_task_as_vtodo.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *
from coils.core.logic import GetCommand
from coils.core.icalendar import Render

class GetTaskAsVToDo(GetCommand):
    __domain__ = 'task'
    __operation__ = 'get-as-vtodo'
    mode = None

    def __init__(self):
        GetCommand.__init__(self)

    def parse_parameters(self, **params):
        if params.has_key('object'):
            self.data = [
             params['object']]
        elif params.has_key('objects'):
            self.data = params['objects']
        else:
            raise 'No tasks provided to command.'

    def run(self):
        if self.data is None:
            self._result = None
        self._result = Render.render(self.data, self._ctx)
        return