# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/legions/statusbar.py
# Compiled at: 2020-05-07 10:49:55
# Size of source mod 2**32: 885 bytes
from pygments.token import Token
import legions.context as context
from nubia import statusbar

class LegionStatusBar(statusbar.StatusBar):

    def __init__(self, context):
        self._last_status = None

    def get_rprompt_tokens(self):
        if self._last_status:
            return [
             (
              Token.RPrompt, 'Error: {}'.format(self._last_status))]
        return []

    def set_last_command_status(self, status):
        self._last_status = status

    def get_tokens(self):
        spacer = (
         Token.Spacer, '  ')
        if context.get_context().verbose:
            is_verbose = (
             Token.Warn, 'ON')
        else:
            is_verbose = (
             Token.Info, 'OFF')
        return [(Token.Toolbar, 'Legions'),
         spacer,
         (
          Token.Toolbar, 'Verbose '),
         spacer,
         is_verbose]