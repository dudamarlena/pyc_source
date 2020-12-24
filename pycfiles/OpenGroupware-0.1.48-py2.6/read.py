# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/actions/format/read.py
# Compiled at: 2012-10-12 07:02:39
import os
from coils.core import *
from coils.core.logic import ActionCommand

class ReadAction(ActionCommand):
    __domain__ = 'action'
    __operation__ = 'read'
    __aliases__ = ['readAction']

    def __init__(self):
        ActionCommand.__init__(self)

    def do_action(self):
        format = self._ctx.run_command('format::get', name=self._format)
        format.process_in(self.rfile, self.wfile)
        self.wfile.flush()
        if self._reject_label is not None:
            self.log.debug(('Storing rejected records in message labeled {0}').format(self._reject_label))
            self.store_in_message(self._reject_label, format.reject_buffer)
        return

    def parse_action_parameters(self):
        self._format = self.action_parameters.get('format', 'StandardRaw')
        self._reject_label = self.action_parameters.get('rejectionsLabel', None)
        return