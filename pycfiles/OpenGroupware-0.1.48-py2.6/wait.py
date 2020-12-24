# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/actions/flow/wait.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from coils.core.logic import ActionCommand

class WaitAction(ActionCommand):
    __domain__ = 'action'
    __operation__ = 'wait'
    __aliases__ = ['waitAction']

    def __init__(self):
        ActionCommand.__init__(self)

    def do_action(self):
        message = self._ctx.run_command('message::get', process=self.process, label=self._wait_for)
        self.log.debug(('Message retrieval in wait returned {0}').format(message))
        if message is None:
            self._continue = False
            self._proceed = False
        return

    def parse_action_parameters(self):
        self._wait_for = self.action_parameters.get('waitForLabel', 'InputMessage')

    def do_epilogue(self):
        pass