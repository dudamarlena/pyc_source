# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/actions/doc/lpr_print.py
# Compiled at: 2012-10-12 07:02:39
import shutil
from subprocess import Popen, PIPE
from coils.core import *
from coils.core.logic import ActionCommand
from coils.foundation.api.printing import LPR

class PrintToLPRAction(ActionCommand):
    __domain__ = 'action'
    __operation__ = 'print-to-lpr'
    __aliases__ = ['printToLPR', 'printToLPRAction']

    def __init__(self):
        ActionCommand.__init__(self)

    @property
    def result_mimetype(self):
        return 'application/postscript'

    def do_action(self):
        if self._convert == 'YES':
            if self.input_message.mimetype == 'application/pdf':
                converter = Popen(['/usr/bin/pdftops', '-', '-'], stdin=PIPE, stdout=self._wfile)
                converter_in, converter_out = converter.stdin, converter.stdout
                shutil.copyfileobj(self._rfile, converter_in)
                converter_in.close()
            elif self.input_message.mimetype == 'application/postscript':
                shutil.copyfileobj(self._rfile, self._wfile)
            else:
                raise CoilsException(('Unsupported input MIME type of "{0}"').format(self.input_message.mimetype))
        else:
            shutil.copyfileobj(self._rfile, self._wfile)
        self._wfile.flush()
        self._wfile.seek(0)
        lpr = LPR(self._server, user=self._ctx.login)
        lpr.connect()
        lpr.send_stream(self._queue, self.input_message.uuid, self._wfile, job_name=self._job_name)
        lpr.close()

    def parse_action_parameters(self):
        self._server = self.action_parameters.get('serverName', 'localhost')
        self._job_name = self.process_label_substitutions(self.action_parameters.get('jobName', None))
        self._queue = self.process_label_substitutions(self.action_parameters.get('printerName', ''))
        self._convert = self.process_label_substitutions(self.action_parameters.get('typeConvert', 'YES'))
        return

    def do_epilogue(self):
        pass