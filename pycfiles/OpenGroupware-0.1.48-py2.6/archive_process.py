# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/archive_process.py
# Compiled at: 2012-10-12 07:02:39
import shutil
from coils.core import *
from utility import filename_for_versioned_process_code

class ArchiveProcess(Command):
    __domain__ = 'process'
    __operation__ = 'archive'

    def parse_parameters(self, **params):
        Command.parse_parameters(self, **params)
        if 'process' in params:
            self._process = params.get('process').object_id
        elif 'pid' in params:
            self._process = self._ctx.run_command('process::get', id=int(params.get('pid')))
        else:
            raise CoilsException('Request to archive process with no PID')

    def run(self):
        get_filename = filename_for_versioned_process_code
        rfile = BLOBManager.Open(get_filename(self._process.object_id, self._process.version), 'r', encoding='binary')
        self._process.version += 1
        wfile = BLOBManager.Create(get_filename(self._process.object_id, self._process.version), encoding='binary')
        shutil.copyfileobj(rfile, wfile)
        BLOBManager.Close(rfile)
        BLOBManager.Close(wfile)
        self._process.status = 'archived'
        self.set_return_value(True)