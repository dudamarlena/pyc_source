# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/openxshareble/app.py
# Compiled at: 2016-06-13 23:52:40
import Adafruit_BluefruitLE
from Adafruit_BluefruitLE.services import UART as OriginalUART
from ble.uart import UART
from ble.readdata import Device
import time, atexit, logging
log = logging.getLogger(__name__)

class App(object):
    """ A high level application object.

  Any application needing to talk to Dexcom G4 + Share will need
  to perform operations to setup the ble data transport.  This class
  mixes the UART, ble code, and provides helpful prolog and epilog
  routines that run before and after main, respectively.
  """

    def __init__(self, **kwds):
        self.disconnect_on_after = kwds.get('disconnect_on_after', False)

    def setup_ble(self):
        self.remote = None
        self.ble = Adafruit_BluefruitLE.get_provider()
        self.ble.initialize()
        self.adapter = self.ble.get_default_adapter()
        self.adapter.power_on()
        log.info(('Using adapter: {0}').format(self.adapter.name))
        self.dexcom = None
        return

    def setup_dexcom(self, serial=None, mac=None):
        try:
            log.info('Discovering services...')
            UART.discover(self.remote)
            self.uart = UART(self.remote, SERIAL=serial)
            self.dexcom = Device(self.uart)
            if not self.dexcom:
                self.dexcom = Device(self.uart)
        except:
            if self.disconnect_on_after:
                self.remote.disconnect()

    def prolog(self, clear_cached_data=True, disconnect_devices=True, scan_devices=True, connect=True, mac=None):
        """
    Things to do before running the main part of the application.
    """
        if clear_cached_data:
            self.ble.clear_cached_data()
        if disconnect_devices:
            log.info('Disconnecting any connected UART devices...')
            UART.disconnect_devices()
        if scan_devices:
            log.info('Searching for UART device...')
            try:
                if mac:
                    self.remote = self.select_mac(mac=mac)
                else:
                    self.adapter.start_scan()
                    self.remote = UART.find_device()
                if self.remote is None:
                    raise RuntimeError('Failed to find UART device!')
            finally:
                if self.adapter.is_scanning:
                    self.adapter.stop_scan()

        if connect and not self.remote.is_connected:
            log.info('Connecting to device...')
            self.remote.connect()
        log.info(self.remote.name)
        for service in self.remote.list_services():
            log.info('services: %s %s', service, service.uuid)

        log.info('ADVERTISED')
        log.info(self.remote.advertised)
        return

    def select_mac(self, mac=None, **kwds):
        for device in self.enumerate_dexcoms(**kwds):
            if str(device.id) == mac:
                return device

    def enumerate_dexcoms(self, timeout_secs=10):
        self.adapter.start_scan()

        def maybe_stop():
            if self.adapter.is_scanning:
                self.adapter.stop_scan()

        log.info('Searching for UART devices...')
        start = time.time()
        now = time.time()
        known_uarts = set()
        while now - start < timeout_secs:
            found = set(UART.find_devices())
            new = found - known_uarts
            for device in new:
                log.info(('Found UART: {0} [{1}]').format(device.name, device.id))

            known_uarts.update(new)
            time.sleep(1.0)
            now = time.time()

        self.adapter.stop_scan()
        return known_uarts

    def epilog(self):
        """
    Things to do after running the main part of the application.
    """
        if self.disconnect_on_after and self.remote.is_connected:
            self.remote.disconnect()

    def set_handler(self, handler):
        self.handler = handler

    def run(self):
        self.ble.run_mainloop_with(self.main)

    def main(self):
        """
    Subclasses should replace this method.
    """
        pass