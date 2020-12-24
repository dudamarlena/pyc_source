# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/watchm8/dispatchers/core.py
# Compiled at: 2017-09-11 04:30:52
from ._base import BaseDispatcher

class Sequential(BaseDispatcher):

    def __init__(self, actions, stop_on_failure=True):
        BaseDispatcher.__init__(self, actions)
        self._stop_on_failure = stop_on_failure

    def fire(self, event, emitter):
        for action in self._actions:
            try:
                action(event, emitter)
            except Exception as e:
                self._log.warning('Action %s failed: %s' % (action, e))
                if self._stop_on_failure is True:
                    self._log.warning('Canceling action dispatcher.')
                    break