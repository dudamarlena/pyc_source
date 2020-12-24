# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/fw/development/AutoBuddy/aioouimeaux/aioouimeaux/device/switch.py
# Compiled at: 2017-11-22 04:31:08
# Size of source mod 2**32: 823 bytes
import asyncio as aio
from aioouimeaux.device import Device

class Switch(Device):
    device_type = 'Switch'

    def __repr__(self):
        return '<WeMo Switch "{}">'.format(self.name)

    def set_state(self, state):
        """
        Set the state of this device to on or off.
        """
        return self.basicevent.SetBinaryState(BinaryState=(int(state)))

    def off(self):
        """
        Turn this device off. If already off, will return "Error".
        """
        return self.set_state(0)

    def on(self):
        """
        Turn this device on. If already on, will return "Error".
        """
        return self.set_state(1)

    def toggle(self):
        """
        Toggle the switch's state.
        """
        return self.set_state(not self.get_state())