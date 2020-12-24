# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/postlund/pyatv_dev/pyatv/pyatv/conf.py
# Compiled at: 2019-10-07 03:42:42
# Size of source mod 2**32: 5929 bytes
__doc__ = 'Configuration when connecting to an Apple TV.'
from pyatv import convert
from pyatv.const import PROTOCOL_MRP, PROTOCOL_DMAP, PROTOCOL_AIRPLAY
_SUPPORTED_PROTOCOLS = [
 PROTOCOL_MRP, PROTOCOL_DMAP]

class AppleTV:
    """AppleTV"""

    def __init__(self, address, device_id, name, **kwargs):
        """Initialize a new AppleTV."""
        self.address = address
        self.name = name
        self.device_id = device_id
        self._services = {}
        self._supported_protocols = kwargs.get('supported_services', _SUPPORTED_PROTOCOLS)

    def add_service(self, service):
        """Add a new service.

        If the service already exists, it will be replaced.
        """
        if service.protocol in self._services:
            existing = self._services[service.protocol]
            if not existing.superseeded_by(service):
                return
        self._services[service.protocol] = service

    def get_service(self, protocol):
        """Look up a service based on protocol.

        If a service with the specified protocol is not available, None is
        returned.
        """
        return self._services.get(protocol, None)

    def services(self):
        """Return all supported services."""
        return list(self._services.values())

    def usable_service(self):
        """Return a usable service or None if there is none.

        A service is usable if enough configuration to be able to make a
        connection is available. If several protocols are usable, MRP will be
        preferred over DMAP.
        """
        services = self._services
        for protocol in self._supported_protocols:
            if protocol in services:
                if services[protocol].is_usable():
                    return services[protocol]

    def is_usable(self):
        """Return True if there are any usable services."""
        return any([x.is_usable() for x in self._services.values()])

    def airplay_service(self):
        """Return service used for AirPlay.

        If no AirPlay service has been found, a default at port 7000 will be
        created.
        """
        if PROTOCOL_AIRPLAY in self._services:
            return self._services[PROTOCOL_AIRPLAY]
        else:
            return AirPlayService(7000)

    def __eq__(self, other):
        """Compare instance with another instance."""
        if isinstance(other, self.__class__):
            return self.device_id == other.device_id
        else:
            return False

    def __str__(self):
        """Return a string representation of this object."""
        services = [' - {0}'.format(s) for s in self._services.values()]
        return '    Name: {0}\n Address: {1}\n      Id: {2}\nServices:\n{3}'.format(self.name, self.address, self.device_id, '\n'.join(services))


class BaseService:
    """BaseService"""

    def __init__(self, protocol, port):
        """Initialize a new BaseService."""
        self.protocol = protocol
        self.port = port

    @staticmethod
    def is_usable():
        """Return True if service is usable, else False."""
        return False

    @staticmethod
    def superseeded_by(other_service):
        """Return True if input service should be used instead of this one."""
        return False

    def __str__(self):
        """Return a string representation of this object."""
        return 'Protocol: {0}, Port: {1}'.format(convert.protocol_str(self.protocol), self.port)


class DmapService(BaseService):
    """DmapService"""

    def __init__(self, device_credentials, port=None):
        """Initialize a new DmapService."""
        super().__init__(PROTOCOL_DMAP, port or 3689)
        self.device_credentials = device_credentials

    def is_usable(self):
        """Return True if service is usable, else False."""
        return self.device_credentials is not None

    def superseeded_by(self, other_service):
        """Return True if input service has login id and this has not."""
        if not other_service or other_service.__class__ != self.__class__ or other_service.protocol != self.protocol or other_service.port != self.port:
            return False
        else:
            return not self.device_credentials and other_service.device_credentials

    def __str__(self):
        return super().__str__() + ', Credentials: {0}'.format(self.device_credentials)


class MrpService(BaseService):
    """MrpService"""

    def __init__(self, port, device_credentials=None):
        """Initialize a new MrpService."""
        super().__init__(PROTOCOL_MRP, port)
        self.device_credentials = device_credentials

    def is_usable(self):
        """Return True if service is usable, else False."""
        return True

    def __str__(self):
        return super().__str__() + ', Credentials: {0}'.format(self.device_credentials)


class AirPlayService(BaseService):
    """AirPlayService"""

    def __init__(self, port):
        super().__init__(PROTOCOL_AIRPLAY, port)