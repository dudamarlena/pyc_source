# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mdt/devices.py
# Compiled at: 2019-09-10 14:32:03
# Size of source mod 2**32: 2194 bytes
"""
Copyright 2019 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from time import sleep
from mdt.discoverer import Discoverer
from mdt.config import Config

class DevicesCommand:
    __doc__ = 'Usage: mdt devices\n\nReturns a list of device names and IP addresses found on the local network\nsegment. Also indicates if a given device is marked as your default.\n\nVariables used:\n   preferred-device: contains the device name you want as your default.\n                     Can be set to an IPv4 address to bypass the mDNS lookup.\n\nNote: MDT uses a python implementation of mDNS ZeroConf for discovery, so\nit does not require a running Avahi daemon.\n'

    def __init__(self):
        self.discoverer = Discoverer()
        self.device = Config().preferredDevice()

    def run(self, args):
        self.discoverer.discover()
        discoveries = self.discoverer.discoveries
        for host, address in discoveries.items():
            if self.device and host == self.device:
                print('{0}\t\t({1},default)'.format(host, address))
            else:
                print('{0}\t\t({1})'.format(host, address))


class DevicesWaitCommand:
    __doc__ = 'Usage: mdt wait-for-device\n\nWaits until a device is found.\n'

    def __init__(self):
        self.found_devices = False
        self.discoverer = Discoverer(self)

    def add_device(self, hostname, address):
        self.found_devices = True
        self.hostname = hostname
        self.address = address

    def run(self, args):
        print('Waiting for device...')
        while not self.found_devices:
            self.discoverer.discover()

        print('Found {0} devices.'.format(len(self.discoverer.discoveries)))
        return 0