# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/aioble/centralmanager.py
# Compiled at: 2019-06-13 01:58:06
# Size of source mod 2**32: 631 bytes
import asyncio

class CentralManager(object):
    """CentralManager"""

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