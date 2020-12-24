# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/foundation/set_alarm.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *

class SetAlarm(Command):
    __domain__ = 'clock'
    __operation__ = 'set-alarm'

    def parse_parameters(self, **params):
        Command.parse_parameters(self, **params)
        self._time = params.get('time', None)
        self._target = params.get('target', None)
        self._source = params.get('source', None)
        self._callback = params.get('callback', None)
        if self._target is None:
            self._target = self._source
        if self._time is None:
            raise CoilsException('No time specified for alarm.')
        return

    def run(self):
        self._result = self._ctx.send(self._source, ('coils.clock/setalarm:{0}').format(self._time), {'alarmTarget': self._target}, callback=self._callback)