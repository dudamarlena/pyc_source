# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/actions/flow/queue.py
# Compiled at: 2012-10-12 07:02:39
import shutil
from tempfile import mkstemp
from coils.core import *
from coils.core.logic import ActionCommand

class QueueProcessAction(ActionCommand):
    __domain__ = 'action'
    __operation__ = 'queue-process'
    __aliases__ = ['queueProcess', 'queueProcessAction']

    def __init__(self):
        ActionCommand.__init__(self)

    @property
    def result_mimetype(self):
        return 'text/plain'

    def do_action(self):
        input_handle = BLOBManager.ScratchFile(suffix='.message')
        shutil.copyfileobj(self.rfile, input_handle)
        route = self._ctx.run_command('route::get', name=self._route_name)
        if route is not None:
            process = self._ctx.run_command('process::new', values={'route_id': route.object_id, 'handle': input_handle})
            process.state = 'Q'
            process.priority = self._priority
            self.wfile.write(unicode(process.object_id))
        else:
            raise CoilsException(('No such route as {0}').format(self._route_name))
        BLOBManager.Close(input_handle)
        return

    def parse_action_parameters(self):
        self._route_name = self.action_parameters.get('routeName', None)
        self._priority = int(self.action_parameters.get('priority', 100))
        if self._route_name is None:
            raise CoilsException('No such route to queue process.')
        return

    def do_epilogue(self):
        ActionCommand.do_epilogue(self)