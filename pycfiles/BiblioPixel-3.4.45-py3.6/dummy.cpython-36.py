# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/drivers/dummy.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 677 bytes
from .driver_base import DriverBase
import time

class Dummy(DriverBase):
    __doc__ = 'For Testing: Provides no ouput, just a valid interface'

    def __init__(self, num=1024, delay=0, **kwds):
        """
        Args
            delay: time to wait in seconds to simulate actual hardware
            interface time
        """
        super().__init__(num)
        self._kwds = kwds
        self._delay = delay

    def _compute_packet(self):
        if self._delay > 0:
            self.clock.sleep(self._delay)


from ..util import deprecated
if deprecated.allowed():
    DriverDummy = Dummy