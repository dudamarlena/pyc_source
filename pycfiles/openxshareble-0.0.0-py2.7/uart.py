# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/openxshareble/ble/uart.py
# Compiled at: 2016-06-13 23:52:40
import Adafruit_BluefruitLE
from Adafruit_BluefruitLE.services import UART as OriginalUART
import Queue, uuid, time
from attrs import Attrs
import logging
log = logging.getLogger(__name__)

class ShareUART(OriginalUART):
    ADVERTISED = [
     Attrs.CradleService]
    SERVICES = [
     Attrs.CradleService]
    CHARACTERISTICS = [Attrs.AuthenticationCode, Attrs.Command, Attrs.Response, Attrs.ShareMessageReceiver, Attrs.ShareMessageResponse, Attrs.HeartBeat, Attrs.DeviceService, Attrs.PowerLevel]
    UART_SERVICE_UUID = Attrs.CradleService
    TX_CHAR_UUID = Attrs.Command
    RX_CHAR_UUID = Attrs.Response


class Share2UART(OriginalUART):
    ADVERTISED = [
     Attrs.VENDOR_UUID]
    SERVICES = [
     Attrs.VENDOR_UUID, Attrs.DeviceService]
    CHARACTERISTICS = []
    HEARTBEAT_UUID = Attrs.HeartBeat2
    UART_SERVICE_UUID = Attrs.VENDOR_UUID
    TX_CHAR_UUID = Attrs.ShareMessageReceiver2
    RX_CHAR_UUID = Attrs.ShareMessageResponse2
    SendDataUUID = Attrs.ShareMessageReceiver2
    RcveDataUUID = Attrs.ShareMessageResponse2
    CommandUUID = Attrs.Command2
    ResponseUUID = Attrs.Response2
    AUTH_UUID = Attrs.AuthenticationCode2

    def __init__(self, device, **kwds):
        """Initialize UART from provided bluez device."""
        log = logging.getLogger(__name__)
        self.log = log.getChild('uart')
        self._uart = device.find_service(self.UART_SERVICE_UUID)
        log.info('UART %s', self._uart)
        self._queue = Queue.Queue()
        r = device.is_paired
        self.serial = kwds.pop('SERIAL', None)
        log.info('paired? %s', r)
        if not r:
            log.info('pairing...')
            device.pair()
            log.info('paired')
            log.info(device.advertised)
            log.info('finding service')
            self._uart = device.find_service(self.UART_SERVICE_UUID)
            log.info('SERVICE %s', self._uart)
            self.pair_auth_code(self.serial)
        self.setup_dexcom()
        return

    def set_serial(self, SERIAL):
        self.serial = SERIAL

    def pair_auth_code(self, serial):
        self.log.info('sending auth code %s', serial)
        self._auth = self._uart.find_characteristic(self.AUTH_UUID)
        self.log.info(self._auth)
        msg = bytearray(serial + '000000')
        self._auth.write_value(str(msg))

    def setup_dexcom_heartbeat(self):
        self._heartbeat = self._uart.find_characteristic(self.HEARTBEAT_UUID)

    def do_heartbeat(self):
        if not self._heartbeat.notifying:
            self._heartbeat.start_notify(self._heartbeat_tick)

    def setup_dexcom(self):
        self.remainder = bytearray()
        self._tx = self._uart.find_characteristic(self.TX_CHAR_UUID)
        self._rx = self._uart.find_characteristic(self.RX_CHAR_UUID)
        self.setup_dexcom_heartbeat()
        self.do_heartbeat()
        self._char_rcv_data = self._uart.find_characteristic(self.RcveDataUUID)
        if self._rx.notifying:
            self._rx.stop_notify()
        if not self._rx.notifying:
            self._rx.start_notify(self._rx_received)

    def _heartbeat_tick(self, data):
        self.log.info('_heartbeat_tick %s', str(data).encode('hex'))

    def _on_rcv(self, data):
        self.log.info('_on_rcv %s', str(data).encode('hex'))

    def read(self, size=1, timeout_sec=None):
        spool = bytearray()
        spool.extend(self.remainder)
        self.remainder = bytearray()
        while len(spool) < size:
            spool.extend(self.pop(timeout_sec=timeout_sec))
            time.sleep(0.1)

        self.remainder.extend(spool[size:])
        return str(spool[:size])

    def pop(self, timeout_sec=None):
        return super(Share2UART, self).read(timeout_sec=timeout_sec)


class BothShare(ShareUART):
    ADVERTISED = ShareUART.ADVERTISED + Share2UART.ADVERTISED
    SERVICES = ShareUART.SERVICES + Share2UART.SERVICES
    CHARACTERISTICS = ShareUART.SERVICES + Share2UART.SERVICES
    UART_SERVICE_UUID = Attrs.CradleService2
    TX_CHAR_UUID = Attrs.Command2
    RX_CHAR_UUID = Attrs.Response2


class UART(Share2UART):
    pass