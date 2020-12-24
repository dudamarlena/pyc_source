# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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