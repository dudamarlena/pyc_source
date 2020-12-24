# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/packagetrack/__init__.py
# Compiled at: 2010-07-14 13:21:08
import os.path
from ConfigParser import ConfigParser
from .ups import UPSInterface
from .fedex import FedexInterface
from .usps import USPSInterface
__version__ = '0.2'
_interfaces = {}
config = ConfigParser()
config.read([os.path.expanduser('~/.packagetrack')])

def register_interface(shipper, interface):
    global _interfaces
    _interfaces[shipper] = interface


def get_interface(shipper):
    if shipper in _interfaces:
        return _interfaces[shipper]
    raise UnsupportedShipper


register_interface('UPS', UPSInterface())
register_interface('FedEx', FedexInterface())
register_interface('USPS', USPSInterface())

class UnsupportedShipper(Exception):
    pass


class Package(object):

    def __init__(self, tracking_number):
        self.tracking_number = tracking_number
        self.shipper = None
        for (shipper, iface) in _interfaces.iteritems():
            if iface.identify(self.tracking_number):
                self.shipper = shipper
                break

        return

    def track(self):
        return get_interface(self.shipper).track(self.tracking_number)

    def url(self):
        return get_interface(self.shipper).url(self.tracking_number)