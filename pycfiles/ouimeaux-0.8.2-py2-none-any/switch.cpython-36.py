# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ian/src/github.com/iancmcc/ouimeaux/ouimeaux/device/switch.py
# Compiled at: 2018-08-26 09:51:15
# Size of source mod 2**32: 980 bytes
import gevent
from ouimeaux.device import Device

class Switch(Device):

    def set_state(self, state):
        """
        Set the state of this device to on or off.
        """
        self.basicevent.SetBinaryState(BinaryState=(int(state)))
        self._state = int(state)

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

    def blink(self, delay=1):
        """
        Toggle the switch once, then again after a delay (in seconds).
        """
        self.toggle()
        gevent.spawn_later(delay, self.toggle)

    def __repr__(self):
        return '<WeMo Switch "{name}">'.format(name=(self.name))