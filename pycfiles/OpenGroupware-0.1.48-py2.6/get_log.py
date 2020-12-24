# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/actions/gw/get_log.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from coils.core.logic import ActionCommand

class GetEntityLogAction(ActionCommand):
    __domain__ = 'action'
    __operation__ = 'get-entity-log'
    __aliases__ = ['getEntityLogAction', 'getEntityLog']

    def __init__(self):
        ActionCommand.__init__(self)

    def do_action(self):
        entries = self._ctx.run_command('object::get-logs', id=self._id)
        for entry in entries:
            self.wfile.write(('{0} {1} {2} {3}\r\n').format(entry.object_id, entry.datetime.strftime('%Y-%m-%d %H:%M:%S UTC'), entry.action, entry.actor_id))
            self.wfile.write(('{0}\r\n').format(entry.message))
            self.wfile.write('\r\n')

    @property
    def result_mimetype(self):
        return 'text/plain'

    def parse_action_parameters(self):
        self._id = int(self.action_parameters.get('objectId', self.pid))

    def do_epilogue(self):
        pass