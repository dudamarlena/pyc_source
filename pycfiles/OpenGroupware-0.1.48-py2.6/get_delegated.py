# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/task/get_delegated.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.foundation import *
from coils.core import *

class GetDelegatedList(Command):
    __domain__ = 'task'
    __operation__ = 'get-delegated'
    mode = None

    def __init__(self):
        Command.__init__(self)

    def parse_parameters(self, **params):
        Command.parse_parameters(self, **params)

    def run(self, **params):
        self.disable_access_check()
        db = self._ctx.db_session()
        self.parse_parameters(**params)
        query = db.query(Task).filter(and_(Task.owner_id.in_(self._ctx.context_ids), Task.state != '30_archived', Task.executor_id != self._ctx.account_id))
        data = query.all()
        if self.access_check:
            data = self._ctx.access_manager.filter_by_access('r', data)
        self.log.debug('%d tasks in result' % len(data))
        self._result = data