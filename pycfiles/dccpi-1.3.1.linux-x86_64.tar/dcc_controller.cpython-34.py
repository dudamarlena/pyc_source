# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python3.4/site-packages/dccpi/dcc_controller.py
# Compiled at: 2016-11-05 00:32:57
# Size of source mod 2**32: 6283 bytes
"""
    Copyright (C) 2016  Hector Sanjuan

    This file is part of "dccpi".

    "dccpi" is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    "dccpi" is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with "dccpi".  If not, see <http://www.gnu.org/licenses/>.
"""
import time, threading, sys

class DCCController(object):
    __doc__ = '\n    A DCC controller take care of generating the packages and sending\n    them using a DCCEncoder of choice.\n\n    It allows to register DCCLocomotives and runs a separate thread\n    to send them packages.\n    '

    def __init__(self, dcc_encoder):
        """
        Initialize the controller. We need to have an encoder instance for that
        """
        self.dcc_encoder = dcc_encoder
        self._state = 'idle'
        self._abort = False
        self.devices = {}
        self._thread = None
        self.devices_lock = threading.Lock()

    def __str__(self):
        'DCC Controller. %i locos managed' % self.devices.keys()

    def __repr__(self):
        str = 'DCC Controller:\n'
        str += '-----------------------------'
        if sys.version_info.major < 3:
            items = self.devices.iteritems()
        else:
            items = self.devices.items()
        for n, device in items:
            str += device.__repr__()
            str += '-----------------------------'

        return str

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new):
        if self._state != new:
            self._state = new

    def register(self, dcc_device):
        dcc_device.notify_update_callback = self.update_payload
        self.devices[dcc_device.name] = dcc_device
        print('%s registered on address #%s' % (dcc_device.name,
         dcc_device.address))
        self.update_payload()

    def unregister(self, dcc_device):
        if type(dcc_device) is str:
            self.devices[dcc_device].notify_update_callback = None
            del self.devices[dcc_device]
        else:
            del self.devices[dcc_device.name]
            dcc_device.notify_update_callback = None
        print('%s has been unregistered' % dcc_device.name)
        self.update_payload()

    def update_payload(self, device_name='*'):
        packets = []
        if sys.version_info.major < 3:
            items = self.devices.iteritems()
        else:
            items = self.devices.items()
        for name, device in self.devices.items():
            packets += device.control_packets()

        self.dcc_encoder.payload = packets

    def start(self):
        if self._thread:
            print('DCC Controller already running')
            return
        print('Starting DCC Controller')
        self._thread = DCCControllerThread(self)
        self._abort = False
        self.state = 'startup'
        self._thread.start()

    def stop(self):
        self._abort = True
        if self._thread:
            self._thread.join()
            self._thread = None
            print('DCC Controller stopped')
        else:
            print('DCC Controller not running')


class DCCControllerThread(threading.Thread):
    __doc__ = '\n    Runs the thread.\n\n    It uses a small state machine to control state:\n      * Startup: broadcast reset packet\n      * New payload: send control packets payload\n      * Shutdown: broadcast stop packet\n      * Idle: send idle packets\n    '

    def __init__(self, dcc_controller):
        self.dcc_controller = dcc_controller
        self.dcc_encoder = dcc_controller.dcc_encoder
        threading.Thread.__init__(self)

    def run(self):
        try:
            idle_count = 0
            while True:
                state = self.dcc_controller.state
                abort = self.dcc_controller._abort
                if abort:
                    state = 'shutdown'
                if state is 'idle':
                    self.dcc_encoder.send_idle(1)
                    idle_count += 1
                    if idle_count >= 1:
                        self.dcc_controller.state = 'newpayload'
                else:
                    if state is 'startup':
                        self.dcc_encoder.tracks_power_on()
                        self.dcc_encoder.send_reset(2)
                        self.dcc_controller.state = 'newpayload'
                    else:
                        if state is 'shutdown':
                            self.dcc_encoder.send_stop(2)
                            self.dcc_encoder.send_reset(2)
                            self.dcc_encoder.tracks_power_off()
                            break
                        else:
                            if state is 'newpayload':
                                self.dcc_encoder.send_payload(15)
                                self.dcc_controller.state = 'idle'
                                idle_count = 0
                            else:
                                sys.stderr.write('Unknown state %s!' % state)
                                self.dcc_controller.state = 'shutdown'
                time.sleep(0.008)

        except:
            self.dcc_encoder.tracks_power_off()
            m = 'An exception ocurred! Please stop the controller!'
            sys.stderr.write(m)
            raise