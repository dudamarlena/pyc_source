# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/animation/off.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 412 bytes
from .animation import Animation

class Off(Animation):
    __doc__ = 'A trivial animation that turns all pixels in a layout off.'

    def __init__(self, layout, timeout=1, **kwds):
        (super().__init__)(layout, **kwds)
        self.internal_delay = timeout

    def step(self, amt=1):
        self.layout.all_off()


from ..util import deprecated
if deprecated.allowed():
    OffAnim = Off