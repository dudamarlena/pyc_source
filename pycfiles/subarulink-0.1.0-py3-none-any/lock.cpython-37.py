# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/data/proj/subarulink/subarulink/lock.py
# Compiled at: 2020-03-30 09:00:20
# Size of source mod 2**32: 1841 bytes
"""
Python Package for controlling Subaru API.

For more details about this api, please refer to the documentation at
https://github.com/G-Two/subarulink
"""
from subarulink.vehicle import VehicleDevice

class Lock(VehicleDevice):
    __doc__ = 'Home-assistant lock class for Subaru vehicles.\n\n    This is intended to be partially inherited by a Home-Assitant entity.\n    '

    def __init__(self, data, controller):
        super().__init__(data, controller)
        self._Lock__manual_update_time = 0
        self._Lock__lock_state = False
        self.type = 'door lock'
        self.hass_type = 'lock'
        self.name = self._name()
        self.uniq_name = self._uniq_name()
        self.bin_type = 7

    async def lock(self):
        """Send lock command."""
        data = await self._controller.lock(self._vin)
        if data:
            if data['data']['success']:
                self._Lock__lock_state = True

    async def unlock(self):
        """Send unlock command."""
        data = await self._controller.unlock(self._vin)
        if data:
            if data['data']['success']:
                self._Lock__lock_state = False

    def is_locked(self):
        """Return whether doors are locked.

        Subaru API does not report lock status.  This state cannot be depended on.
        """
        return self._Lock__lock_state

    @staticmethod
    def has_battery():
        """Return whether the device has a battery."""
        return False