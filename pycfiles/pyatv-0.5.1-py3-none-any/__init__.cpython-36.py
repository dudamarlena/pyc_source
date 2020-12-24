# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/postlund/pyatv_dev/pyatv/pyatv/__init__.py
# Compiled at: 2019-10-07 04:28:11
# Size of source mod 2**32: 8589 bytes
"""Library for controlling an Apple TV."""
import asyncio, logging, concurrent
from ipaddress import ip_address
from threading import Lock
from getmac import get_mac_address
from zeroconf import ServiceBrowser, Zeroconf
from aiohttp import ClientSession
from pyatv import conf, exceptions
from pyatv.airplay import player
from pyatv.airplay.api import AirPlayAPI
from pyatv.const import PROTOCOL_MRP, PROTOCOL_DMAP, PROTOCOL_AIRPLAY
from pyatv.net import HttpSession
from pyatv.dmap import DmapAppleTV
from pyatv.mrp import MrpAppleTV
_LOGGER = logging.getLogger(__name__)
HOMESHARING_SERVICE = '_appletv-v2._tcp.local.'
DEVICE_SERVICE = '_touch-able._tcp.local.'
MEDIAREMOTE_SERVICE = '_mediaremotetv._tcp.local.'
AIRPLAY_SERVICE = '_airplay._tcp.local.'

class _ServiceListener:

    def __init__(self, loop, abort_on_found, device_id, protocol, semaphore):
        """Initialize a new _ServiceListener."""
        self.loop = loop
        self.abort_on_found = abort_on_found
        self.device_id = device_id
        self.protocol = protocol
        self.semaphore = semaphore
        self.found_devices = {}
        self.lock = Lock()

    def add_service(self, zeroconf, service_type, name):
        """Handle callback from zeroconf when a service has been discovered."""
        self.lock.acquire()
        try:
            self._internal_add(zeroconf, service_type, name)
        finally:
            self.lock.release()

    def _internal_add(self, zeroconf, service_type, name):
        if self.abort_on_found:
            if len(self.found_devices) == 1:
                return
        else:
            info = zeroconf.get_service_info(service_type, name)
            address = ip_address(info.addresses[0])
            if info.type == HOMESHARING_SERVICE:
                self.add_hs_service(info, address)
            else:
                if info.type == DEVICE_SERVICE:
                    self.add_non_hs_service(info, address)
                else:
                    if info.type == MEDIAREMOTE_SERVICE:
                        self.add_mrp_service(info, address)
                    else:
                        if info.type == AIRPLAY_SERVICE:
                            self.add_airplay_service(info, address)
                        else:
                            _LOGGER.warning('Discovered unknown device: %s', info)

    def add_hs_service(self, info, address):
        """Add a new device to discovered list."""
        if self.protocol:
            if self.protocol != PROTOCOL_DMAP:
                return
        name = info.properties[b'Name'].decode('utf-8')
        hsgid = info.properties[b'hG'].decode('utf-8')
        self._handle_service(address, name, conf.DmapService(hsgid, port=(info.port)))

    def add_non_hs_service(self, info, address):
        """Add a new device without Home Sharing to discovered list."""
        if self.protocol:
            if self.protocol != PROTOCOL_DMAP:
                return
        name = info.properties[b'CtlN'].decode('utf-8')
        self._handle_service(address, name, conf.DmapService(None, port=(info.port)))

    def add_mrp_service(self, info, address):
        """Add a new MediaRemoteProtocol device to discovered list."""
        if self.protocol:
            if self.protocol != PROTOCOL_MRP:
                return
        name = info.properties[b'Name'].decode('utf-8')
        self._handle_service(address, name, conf.MrpService(info.port))

    def add_airplay_service(self, info, address):
        """Add a new AirPlay device to discovered list."""
        if self.protocol:
            if self.protocol != PROTOCOL_AIRPLAY:
                return
        name = info.name.replace('._airplay._tcp.local.', '')
        self._handle_service(address, name, conf.AirPlayService(info.port))

    def _handle_service(self, address, name, service):
        if self.abort_on_found:
            if not service.is_usable():
                _LOGGER.debug('Ignoring unusable device %s', name)
                return
        else:
            if address not in self.found_devices:
                device_id = _get_device_id(str(address))
                if self.device_id:
                    if self.device_id != device_id:
                        _LOGGER.debug('Ignoring %s (not matching %s)', device_id, self.device_id)
                        return
                self.found_devices[address] = conf.AppleTV(address, device_id, name)
            _LOGGER.debug('Auto-discovered %s at %s:%d (protocol: %s)', name, address, service.port, service.protocol)
            atv = self.found_devices[address]
            atv.add_service(service)
            if self._should_abort(address):
                _LOGGER.debug('Aborting since a device was found')
                self.found_devices = {address: atv}
                self.loop.call_soon_threadsafe(self.semaphore.release)

    def _should_abort(self, address):
        if not self.abort_on_found:
            return False
        else:
            return self.found_devices[address].usable_service()


async def scan_for_apple_tvs(loop, timeout=5, abort_on_found=False, device_id=None, only_usable=True, protocol=None):
    """Scan for Apple TVs using zeroconf (bonjour) and returns them."""
    semaphore = asyncio.Semaphore(value=0, loop=loop)
    listener = _ServiceListener(loop, abort_on_found, device_id, protocol, semaphore)
    zeroconf = Zeroconf()
    try:
        try:
            ServiceBrowser(zeroconf, HOMESHARING_SERVICE, listener)
            ServiceBrowser(zeroconf, DEVICE_SERVICE, listener)
            ServiceBrowser(zeroconf, MEDIAREMOTE_SERVICE, listener)
            ServiceBrowser(zeroconf, AIRPLAY_SERVICE, listener)
            _LOGGER.debug('Discovering devices for %d seconds', timeout)
            await asyncio.wait_for((semaphore.acquire()), timeout, loop=loop)
        except concurrent.futures.TimeoutError:
            pass

    finally:
        zeroconf.close()

    def _should_include(atv):
        if not only_usable:
            return True
        else:
            return atv.is_usable()

    found_devices = listener.found_devices.values()
    return [x for x in found_devices if _should_include(x)]


async def connect_to_apple_tv(details, loop, protocol=None, session=None):
    """Connect and logins to an Apple TV."""
    if details.device_id is None:
        raise exceptions.DeviceIdMissingError('missing device id for ' + str(details.address))
    service = _get_service_used_to_connect(details, protocol)
    if session is None:
        session = ClientSession(loop=loop)
    airplay = _setup_airplay(loop, session, details)
    if service.protocol == PROTOCOL_DMAP:
        return DmapAppleTV(loop, session, details, airplay)
    else:
        return MrpAppleTV(loop, session, details, airplay)


def _get_service_used_to_connect(details, protocol):
    if not protocol:
        service = details.usable_service()
    else:
        service = details.get_service(protocol)
    if not service:
        raise exceptions.NoUsableServiceError('no usable service to connect to')
    return service


def _setup_airplay(loop, session, details):
    airplay_service = details.airplay_service()
    airplay_player = player.AirPlayPlayer(loop, session, details.address, airplay_service.port)
    airplay_http = HttpSession(session, 'http://{0}:{1}/'.format(details.address, airplay_service.port))
    return AirPlayAPI(airplay_http, airplay_player)


def _get_device_id(address):
    try:
        mac = get_mac_address(ip=address, network_request=False)
        if mac is not None:
            return mac.lower().replace(':', '')
    except Exception:
        _LOGGER.warning('failed to determine device id for %s', address)


async def get_device_id(address, loop):
    """Get device id for an address.

    This is a convenience method that can be used to look up a
    device id for an address. It is supposed to be used when not relying
    on the builtin scan function (i.e. scan_for_apple_tvs). It is only
    supported when used in conjuction with finding a device with
    python-zeroconf.
    """
    return await loop.run_in_executor(None, _get_device_id, address)