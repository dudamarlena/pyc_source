# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/data/proj/subarulink/subarulink/vehicle.py
# Compiled at: 2020-04-04 15:06:20
# Size of source mod 2**32: 2135 bytes
"""
Python Package for controlling Subaru Starlink API.

For more details about this api, please refer to the documentation at
https://github.com/G-Two/subarulink
"""
import logging, time
_LOGGER = logging.getLogger(__name__)

class VehicleDevice:
    __doc__ = 'Home-assistant class of Subaru vehicles.\n\n    This is intended to be partially inherited by a Home-Assitant entity.\n    '

    def __init__(self, data, controller):
        """Initialize the Vehicle.

        Parameters
        ----------
        data : dict
            Identifier info for a Subaru vehicle.
        controller : subarulink.Controller
            The controller that controls updates to the Subaru API.

        Returns
        -------
        None

        """
        self._id = data['id']
        self._display_name = data['display_name']
        self._vin = data['vin']
        self._controller = controller
        self.should_poll = True
        self.type = 'device'

    def _name(self):
        if self._display_name is not None:
            if self._display_name != self._vin[-6:]:
                return '{} {}'.format(self._display_name, self.type)
        return 'Subaru Model {} {}'.format(str(self._vin[3]).upper(), self.type)

    def _uniq_name(self):
        return 'Subaru Model {} {} {}'.format(str(self._vin[3]).upper(), self._vin[-6:], self.type)

    def id(self):
        """Return the id of this Vehicle."""
        return self._id

    def car_name(self):
        """Return the car name of this Vehicle."""
        return self._display_name

    def vin(self):
        """Return the VIN of this Vehicle."""
        return self._vin

    def assumed_state(self):
        """Return whether the data is current."""
        return not time.time() - self._controller._last_update_time[self._vin] > self._controller.update_interval

    async def async_update(self):
        """Update the car."""
        await self._controller.update(self._vin)