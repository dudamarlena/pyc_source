# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mdt/discoverer.py
# Compiled at: 2019-09-10 14:32:03
# Size of source mod 2**32: 2674 bytes
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
from typing import cast
from zeroconf import ServiceBrowser, Zeroconf
import socket, time

class DeviceNotFoundError(Exception):
    pass


class Discoverer:
    ANNOUNCE_PERIOD_SECS = 1
    MAXIMUM_WAIT_CYCLES = 10
    SERVICE_TYPE = '_googlemdt._tcp.local.'

    def __init__(self, listener=None):
        self.discoveries = {}
        self.listener = listener
        self.zeroconf = None

    def discover(self):
        self.zeroconf = Zeroconf()
        self.browser = ServiceBrowser(self.zeroconf, Discoverer.SERVICE_TYPE, self)
        self._heard_announcement = True
        cycle_count = 0
        while self._heard_announcement and cycle_count < Discoverer.MAXIMUM_WAIT_CYCLES:
            cycle_count += 1
            self._heard_announcement = False
            time.sleep(Discoverer.ANNOUNCE_PERIOD_SECS)

        self.browser.cancel()
        self.browser = None
        self.zeroconf = None

    def add_service(self, zeroconf, type, name):
        info = self.zeroconf.get_service_info(type, name)
        if info:
            hostname = info.server.split('.')[0]
            address = socket.inet_ntoa(cast(bytes, info.address))
            if hostname not in self.discoveries:
                self._heard_announcement = True
            self.discoveries[hostname] = address
            if self.listener:
                if hasattr(self.listener, 'add_device'):
                    self.listener.add_device(hostname, address)

    def remove_service(self, zeroconf, type, name):
        info = self.zeroconf.get_service_info(type, name)
        if info:
            if self.listener:
                if hasattr(self.listener, 'remove_device'):
                    self.listener.remove_device(info.server, self.discoveries[info.server])
            if info.server in self.discoveries:
                self._heard_announcement = True
                del self.discoveries[info.server]