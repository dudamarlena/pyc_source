# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/foundation/get_performance_log.py
# Compiled at: 2012-10-12 07:02:39
from time import time
from coils.core import *

class GetPerformanceLog(Command):
    __domain__ = 'admin'
    __operation__ = 'get-performance-log'

    def parse_parameters(self, **params):
        Command.parse_parameters(self, **params)
        self._lname = params.get('lname', 'logic')
        self._callback = params.get('callback', None)
        return

    def _local_callback(self, uuid, source, target, data):
        self.log.debug('admin:get-performance-log self callback reached.')
        if uuid == self._uuid:
            if data is not None:
                if isinstance(data, dict):
                    if data.get('status', 500) == 200:
                        self._data = data.get('payload', 'No content')
                    else:
                        raise CoilsException('Administrator reports error returning performance log.')
                else:
                    raise CoilsException('Unexpected data type in packet payload from administrator.')
            else:
                raise CoilsException('Administrator responded with packet having no payload.')
            return True
        else:
            return False

    def _wait(self):
        if self._data is None:
            if time() < self._timeout:
                return True
        return False

    def run(self):
        self._data = None
        if self._callback is None:
            self._callback = self._local_callback
            local_callback = True
            self.log.debug('admin::get-performance-log using self callback')
        else:
            local_callback = False
        self._uuid = self._ctx.send(None, ('coils.administrator/get_performance_log:{0}').format(self._lname), None, callback=self._callback)
        if local_callback:
            self._timeout = time() + 10
            self.log.debug(('entering wait @ {0} till {1}').format(time(), self._timeout))
            while self._wait():
                self._ctx.wait(timeout=10000)
                self.log.debug(('resuming wait @ {0}').format(time()))

            self.log.debug(('exited wait @ {0}').format(time()))
            if self._data is None:
                raise CoilsException('No response from coils.administrator')
            else:
                self._result = self._data
        else:
            self._result = self._uuid
        return