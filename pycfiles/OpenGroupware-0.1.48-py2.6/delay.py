# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/actions/flow/delay.py
# Compiled at: 2012-10-12 07:02:39
import time
from coils.core import *
from coils.core.logic import ActionCommand

class DelayAction(ActionCommand):
    __domain__ = 'action'
    __operation__ = 'delay'
    __aliases__ = ['delayAction', 'delay']
    mode = None

    def __init__(self):
        ActionCommand.__init__(self)

    def do_action(self):
        if self._start + self._delay > time.time():
            self._proceed = False

    def parse_action_parameters(self):
        self._delay = int(self.action_parameters.get('delay', 60))
        if self._uuid not in self._state:
            self._state[self._uuid] = {}
            self._state[self._uuid]['start'] = time.time()
        self._start = self._state[self._uuid].get('start')

    def do_epilogue(self):
        pass