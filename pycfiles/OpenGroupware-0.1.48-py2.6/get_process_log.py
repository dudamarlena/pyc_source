# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/get_process_log.py
# Compiled at: 2012-10-12 07:02:39
from time import time
from StringIO import StringIO
from sqlalchemy import and_
from coils.core import *
from utility import filename_for_process_log, read_cached_process_log, delete_cached_process_logs, cache_process_log

class GetProcessLog(Command):
    __domain__ = 'process'
    __operation__ = 'get-log'

    def parse_parameters(self, **params):
        Command.parse_parameters(self, **params)
        self.format = params.get('format', 'text/plain')
        self.obj = params.get('process', params.get('object', None))
        if self.obj is None:
            self.pid = params.get('pid', params.get('id', None))
        else:
            self.pid = self._obj.object_id
        if self.pid is None:
            raise CoilsException('ProcessId required to retreive process OIE proprties')
        return

    def run(self):
        process = self._ctx.run_command('process::get', id=self.pid)
        if process:
            log_text = read_cached_process_log(process.object_id, process.version)
        else:
            raise CoilsException('Could not marshall specified process.')
        db = self._ctx.db_session()
        if not log_text:
            query = db.query(ProcessLogEntry).filter(and_(ProcessLogEntry.process_id == self.pid, ProcessLogEntry.stanza != None)).order_by(ProcessLogEntry.timestamp)
            content = StringIO('')
            stanza = None
            start = None
            for log in query.all():
                if stanza != log.stanza:
                    if stanza is not None:
                        content.write('\n')
                    stanza = log.stanza
                    content.write(('Stanza {0}\n').format(stanza.strip()))
                category = log.category
                if category is None:
                    category = 'info'
                else:
                    category = category.strip()
                    if category == 'start':
                        start = log.timestamp
                content.write(('{0}:{1}\n').format(category.strip(), log.message))
                if category == 'complete' and start is not None:
                    content.write(('duration:{0}s\n').format(log.timestamp - start))
                    start = None

            log_text = content.getvalue()
            content.close()
            content = None
            cache_process_log(process.object_id, process.version, log_text)
        self.set_return_value(log_text)
        return