# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/electrum_chi/electrum/plugins/safe_t/transport.py
# Compiled at: 2019-08-24 06:06:43
# Size of source mod 2**32: 3566 bytes
from electrum.logging import get_logger
_logger = get_logger(__name__)

class SafeTTransport:

    @staticmethod
    def all_transports():
        """Reimplemented safetlib.transport.all_transports so that we can
        enable/disable specific transports.
        """
        try:
            from safetlib.transport import all_transports
        except ImportError:
            transports = []
            try:
                from safetlib.transport_hid import HidTransport
                transports.append(HidTransport)
            except BaseException:
                pass

            try:
                from safetlib.transport_webusb import WebUsbTransport
                transports.append(WebUsbTransport)
            except BaseException:
                pass

        else:
            transports = []
            try:
                from safetlib.transport.hid import HidTransport
                transports.append(HidTransport)
            except BaseException:
                pass

            try:
                from safetlib.transport.webusb import WebUsbTransport
                transports.append(WebUsbTransport)
            except BaseException:
                pass

            return transports
            return transports

    def enumerate_devices(self):
        """Just like safetlib.transport.enumerate_devices,
        but with exception catching, so that transports can fail separately.
        """
        devices = []
        for transport in self.all_transports():
            try:
                new_devices = transport.enumerate()
            except BaseException as e:
                try:
                    _logger.info(f"enumerate failed for {transport.__name__}. error {e}")
                finally:
                    e = None
                    del e

            else:
                devices.extend(new_devices)

        return devices

    def get_transport(self, path=None):
        """Reimplemented safetlib.transport.get_transport,
        (1) for old safetlib
        (2) to be able to disable specific transports
        (3) to call our own enumerate_devices that catches exceptions
        """
        if path is None:
            try:
                return self.enumerate_devices()[0]
            except IndexError:
                raise Exception('No Safe-T mini found') from None

        def match_prefix(a, b):
            return a.startswith(b) or b.startswith(a)

        transports = [t for t in self.all_transports() if match_prefix(path, t.PATH_PREFIX)]
        if transports:
            return transports[0].find_by_path(path)
        raise Exception("Unknown path prefix '%s'" % path)