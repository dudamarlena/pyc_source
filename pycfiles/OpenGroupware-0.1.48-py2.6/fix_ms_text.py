# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/actions/format/fix_ms_text.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from coils.core.logic import ActionCommand

class FixMicrosoftTextAction(ActionCommand):
    __domain__ = 'action'
    __operation__ = 'fix-microsoft-text'
    __aliases__ = ['fixMicrosoftText']

    def __init__(self):
        ActionCommand.__init__(self)

    def do_action(self):
        while 1:
            data_in = self.rfile.read(65535)
            if data_in == '':
                break
            else:
                data_out = fix_microsoft_text(data_in)
                if len(data_in) != len(data_out):
                    raise Exception('Translation caused length of data to change!')
                self.wfile.write(data_out)

    def parse_action_parameters(self):
        pass