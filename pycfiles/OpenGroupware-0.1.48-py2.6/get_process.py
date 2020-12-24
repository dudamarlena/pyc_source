# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/get_process.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *
from coils.core.logic import GetCommand
from utility import filename_for_process_markup

class GetProcess(GetCommand):
    __domain__ = 'process'
    __operation__ = 'get'

    def set_markup(self, processes):
        result = []
        for process in processes:
            try:
                handle = BLOBManager.Open(filename_for_process_markup(process), 'rb', encoding='binary')
            except IOError, e:
                self.log.error(('Unable to load process markup for processId#{0}').format(process.object_id))
                continue
            else:
                if handle is not None:
                    bpml = handle.read()
                    process.set_markup(bpml)
                    BLOBManager.Close(handle)
                    result.append(process)

        return result

    def parse_parameters(self, **params):
        GetCommand.parse_parameters(self, **params)

    def run(self, **params):
        db = self._ctx.db_session()
        if self.query_by == 'object_id':
            if len(self.object_ids) > 0:
                query = db.query(Process).filter(Process.object_id.in_(self.object_ids))
        else:
            self.set_multiple_result_mode()
            query = db.query(Process).filter(Process.owner_id.in_(self._ctx.context_ids))
        self.set_return_value(self.set_markup(query.all()))