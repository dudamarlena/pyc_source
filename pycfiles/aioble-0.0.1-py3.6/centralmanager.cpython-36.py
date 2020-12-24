# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/aioble/centralmanager.py
# Compiled at: 2019-06-13 01:58:06
# Size of source mod 2**32: 631 bytes
import asyncio

class CentralManager(object):
    __doc__ = 'The Central Manager Base Class'

    def __init__(self, loop=None, *args, **kwargs):
        self.loop = loop if loop else asyncio.get_event_loop()

    async def start_scan(self, callback):
        """Start Scan with timeout"""
        raise NotImplementedError()

    async def stop_scan(self):
        """Stop Scan with timeout"""
        raise NotImplementedError()

    async def power_on(self):
        """Power on BLE Adapter"""
        raise NotImplementedError()

    async def power_off(self):
        """Power off BLE Adapter"""
        raise NotImplementedError()