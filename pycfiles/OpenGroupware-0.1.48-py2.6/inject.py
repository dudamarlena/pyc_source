# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/actions/flow/inject.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from coils.core.logic import ActionCommand

class InjectMessageAction(ActionCommand):
    __domain__ = 'action'
    __operation__ = 'inject-message'
    __aliases__ = ['injectMessageAction', 'injectMessage']

    def __init__(self):
        ActionCommand.__init__(self)

    @property
    def result_mimetype(self):
        return self._mimetype

    def do_action(self):
        self.wfile.write(self._message)

    def parse_action_parameters(self):
        self._message = self.action_parameters.get('user_message', None)
        self._mimetype = self.action_parameters.get('mimetype', 'application/octet-string')
        if self._message:
            self._message = self.process_label_substitutions(self._message)
        else:
            self._message = ''
        return

    def do_epilogue(self):
        pass