# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/drivers/text.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 1035 bytes
from .driver_base import DriverBase
from ..colors import names
from ..util import log
import time

class Text(DriverBase):
    __doc__ = 'For testing:  prints colors to terminal'

    def __init__(self, num=1024, columns=8, max_colors=16, **kwds):
        """
        Args
            delay: time to wait in seconds to simulate actual hardware
            interface time
        """
        super().__init__(num)
        self.columns = columns
        self.max_colors = max_colors

    def _compute_packet(self):
        count = self.numLEDs
        if self.max_colors:
            count = min(count, self.max_colors)
        else:
            for i in range(count):
                if not i % self.columns:
                    log.printer()
                hex_color = names.color_to_name(self._colors[(i + self._pos)], True)
                log.printer(hex_color, ' ', end='')

            if self.max_colors and self.numLEDs > self.max_colors:
                log.printer('...')
            else:
                log.printer('')
        log.printer('--')