# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: pyfeld/renderer.py
# Compiled at: 2017-11-23 08:41:51
from __future__ import unicode_literals
from pyfeld.upnpService import UpnpService

class Renderer:

    def __init__(self, udn, name, location):
        self.name = name
        self.udn = udn
        self.upnp_service = None
        self.location = location
        return

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def get_location(self):
        return self.location

    def get_udn(self):
        return self.udn

    def set_upnp_service(self, location):
        self.upnp_service = UpnpService()
        if location is not None:
            self.upnp_service.set_location(location)
        return