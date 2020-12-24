# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/get_messages.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *

class GetMessages(GetCommand):
    __domain__ = 'process'
    __operation__ = 'get-messages'

    def __init__(self):
        GetCommand.__init__(self)
        self.set_multiple_result_mode()

    def parse_parameters(self, **params):
        Command.parse_parameters(self, **params)
        if 'pid' in params:
            self.pid = params['pid']
            self.query_by = 'pid'
        elif 'process' in params:
            self.pid = params['process'].object_id
            self.query_by = 'pid'

    def get_process(self, pid):
        if isinstance(pid, Process):
            return pid
        return self._ctx.run_command('process::get', id=pid, access_check=self.access_check)

    def run(self, **params):
        db = self._ctx.db_session()
        if self.pid is None:
            raise CoilsException('No PID specified for process::get-messages')
        process = self.get_process(self.pid)
        if process is None:
            self.set_return_value([])
            return
            raise CoilsException(('Unable to resolve PID {0}').format(self.pid))
        query = db.query(Message).filter(Message.process_id == process.object_id)
        self._result = []
        self.set_return_value(query.all())
        return