# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/actions/format/write.py
# Compiled at: 2012-10-12 07:02:39
import os
from coils.core import *
from coils.core.logic import ActionCommand

class WriteAction(ActionCommand):
    __domain__ = 'action'
    __operation__ = 'write'
    __aliases__ = ['writeAction']

    def __init__(self):
        ActionCommand.__init__(self)

    def parse_action_parameters(self):
        self._format_name = self.action_parameters.get('format', 'StandardRaw')

    @property
    def result_mimetype(self):
        return self._format.mimetype

    def do_action(self):
        self._format = self._ctx.run_command('format::get', name=self._format_name)
        self._format.process_out(self.rfile, self.wfile)
        self.wfile.flush()