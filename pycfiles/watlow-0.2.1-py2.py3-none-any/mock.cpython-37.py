# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jamesjeffryes/Documents/NuMat/watlow/build/lib/watlow/mock.py
# Compiled at: 2020-02-20 16:03:43
# Size of source mod 2**32: 1104 bytes
import asyncio
from random import random
from copy import deepcopy

class Gateway:
    __doc__ = 'Mock interface to the Watlow Gateway used to communicate with ovens'

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.state = {i:{'actual':25,  'setpoint':25} for i in range(1, 9)}

    def __getattr__(self, attr):

        def handler(*args, **kwargs):
            return False

        return handler

    def _perturb(self):
        """Make the values dance a bit"""
        for temps in self.state.values():
            if temps['actual'] < temps['setpoint']:
                temps['actual'] += 1

    async def get(self, zone):
        """Return a mock state with the same object structure"""
        await asyncio.sleep(random() * 0.25)
        self._perturb()
        return deepcopy(self.state.get(zone))

    async def set_setpoint(self, zone, setpoint):
        """Set a mock state"""
        await asyncio.sleep(random() * 0.25)
        self.state[zone]['setpoint'] = setpoint