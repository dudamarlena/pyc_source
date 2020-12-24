# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/socket_proxy/base.py
# Compiled at: 2020-05-03 07:41:38
# Size of source mod 2**32: 1189 bytes
import enum, ipaddress, logging
from datetime import datetime
_logger = logging.getLogger(__name__)
CLIENT_NAME_SIZE = 8
INTERVAL_TIME = 15
DEFAULT_PORT = 2773
DEFAULT_LOG_LEVEL = 'debug'
LOG_FORMAT = '{asctime} [{levelname:^8}] {message}'
LOG_LEVELS = {'critical':logging.CRITICAL, 
 'debug':logging.DEBUG, 
 'error':logging.ERROR, 
 'info':logging.INFO, 
 'warn':logging.WARN, 
 'warning':logging.WARNING}

class InvalidPackage(Exception):
    pass


class InvalidPackageType(InvalidPackage):
    pass


class DuplicatePackageType(InvalidPackage):
    pass


class ReachedClientLimit(Exception):
    pass


class TransportType(enum.IntEnum):
    IPv4 = 1
    IPv6 = 2

    @staticmethod
    def from_ip(ip):
        if isinstance(ip, (bytes, str)):
            ip = ipaddress.ip_address(ip)
        if isinstance(ip, ipaddress.IPv4Address):
            return TransportType.IPv4
        if isinstance(ip, ipaddress.IPv6Address):
            return TransportType.IPv6
        raise ipaddress.AddressValueError()


class Ban:
    __slots__ = ('first', 'hits')

    def __init__(self):
        self.hits = 0
        self.first = datetime.now()