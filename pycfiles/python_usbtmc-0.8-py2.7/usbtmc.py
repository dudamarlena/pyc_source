# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/usbtmc/usbtmc.py
# Compiled at: 2017-01-18 00:39:08
"""

Python USBTMC driver

Copyright (c) 2012-2017 Alex Forencich

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

"""
import usb.core, usb.util, struct, time, os, re, sys
USBTMC_bInterfaceClass = 254
USBTMC_bInterfaceSubClass = 3
USBTMC_bInterfaceProtocol = 0
USB488_bInterfaceProtocol = 1
USBTMC_MSGID_DEV_DEP_MSG_OUT = 1
USBTMC_MSGID_REQUEST_DEV_DEP_MSG_IN = 2
USBTMC_MSGID_DEV_DEP_MSG_IN = 2
USBTMC_MSGID_VENDOR_SPECIFIC_OUT = 126
USBTMC_MSGID_REQUEST_VENDOR_SPECIFIC_IN = 127
USBTMC_MSGID_VENDOR_SPECIFIC_IN = 127
USB488_MSGID_TRIGGER = 128
USBTMC_STATUS_SUCCESS = 1
USBTMC_STATUS_PENDING = 2
USBTMC_STATUS_FAILED = 128
USBTMC_STATUS_TRANSFER_NOT_IN_PROGRESS = 129
USBTMC_STATUS_SPLIT_NOT_IN_PROGRESS = 130
USBTMC_STATUS_SPLIT_IN_PROGRESS = 131
USB488_STATUS_INTERRUPT_IN_BUSY = 32
USBTMC_REQUEST_INITIATE_ABORT_BULK_OUT = 1
USBTMC_REQUEST_CHECK_ABORT_BULK_OUT_STATUS = 2
USBTMC_REQUEST_INITIATE_ABORT_BULK_IN = 3
USBTMC_REQUEST_CHECK_ABORT_BULK_IN_STATUS = 4
USBTMC_REQUEST_INITIATE_CLEAR = 5
USBTMC_REQUEST_CHECK_CLEAR_STATUS = 6
USBTMC_REQUEST_GET_CAPABILITIES = 7
USBTMC_REQUEST_INDICATOR_PULSE = 64
USB488_READ_STATUS_BYTE = 128
USB488_REN_CONTROL = 160
USB488_GOTO_LOCAL = 161
USB488_LOCAL_LOCKOUT = 162
USBTMC_HEADER_SIZE = 12
RIGOL_QUIRK_PIDS = [
 1230, 1416]

def parse_visa_resource_string(resource_string):
    m = re.match('^(?P<prefix>(?P<type>USB)\\d*)(::(?P<arg1>[^\\s:]+))(::(?P<arg2>[^\\s:]+(\\[.+\\])?))(::(?P<arg3>[^\\s:]+))?(::(?P<suffix>INSTR))$', resource_string, re.I)
    if m is not None:
        return dict(type=m.group('type').upper(), prefix=m.group('prefix'), arg1=m.group('arg1'), arg2=m.group('arg2'), arg3=m.group('arg3'), suffix=m.group('suffix'))
    else:
        return


class UsbtmcException(Exception):
    em = {0: 'No error'}

    def __init__(self, err=None, note=None):
        self.err = err
        self.note = note
        self.msg = ''
        if err is None:
            self.msg = note
        else:
            if type(err) is int:
                if err in self.em:
                    self.msg = '%d: %s' % (err, self.em[err])
                else:
                    self.msg = '%d: Unknown error' % err
            else:
                self.msg = err
            if note is not None:
                self.msg = '%s [%s]' % (self.msg, note)
        return

    def __str__(self):
        return self.msg


def list_devices():
    """List all connected USBTMC devices"""

    def is_usbtmc_device(dev):
        for cfg in dev:
            d = usb.util.find_descriptor(cfg, bInterfaceClass=USBTMC_bInterfaceClass, bInterfaceSubClass=USBTMC_bInterfaceSubClass)
            is_advantest = dev.idVendor == 4916
            return d is not None or is_advantest

        return

    return list(usb.core.find(find_all=True, custom_match=is_usbtmc_device))


def find_device(idVendor=None, idProduct=None, iSerial=None):
    """Find USBTMC instrument"""
    devs = list_devices()
    if len(devs) == 0:
        return
    else:
        for dev in devs:
            if dev.idVendor != idVendor or dev.idProduct != idProduct:
                continue
            if iSerial is None:
                return dev
            s = ''
            try:
                s = dev.serial_number
            except:
                pass

            if iSerial == s:
                return dev

        return


class Instrument(object):
    """USBTMC instrument interface client"""

    def __init__(self, *args, **kwargs):
        """Create new USBTMC instrument object"""
        self.idVendor = 0
        self.idProduct = 0
        self.iSerial = None
        self.device = None
        self.cfg = None
        self.iface = None
        self.term_char = None
        self.advantest_quirk = False
        self.advantest_locked = False
        self.rigol_quirk = False
        self.rigol_quirk_ieee_block = False
        self.bcdUSBTMC = 0
        self.support_pulse = False
        self.support_talk_only = False
        self.support_listen_only = False
        self.support_term_char = False
        self.bcdUSB488 = 0
        self.support_USB4882 = False
        self.support_remote_local = False
        self.support_trigger = False
        self.support_scpi = False
        self.support_SR = False
        self.support_RL = False
        self.support_DT = False
        self.max_transfer_size = 1048576
        self.timeout = 5.0
        self.bulk_in_ep = None
        self.bulk_out_ep = None
        self.interrupt_in_ep = None
        self.last_btag = 0
        self.last_rstb_btag = 0
        self.connected = False
        self.reattach = []
        self.old_cfg = None
        resource = None
        if len(args) == 1:
            if type(args[0]) == str:
                resource = args[0]
            else:
                self.device = args[0]
        if len(args) >= 2:
            self.idVendor = args[0]
            self.idProduct = args[1]
        if len(args) >= 3:
            self.iSerial = args[2]
        for op in kwargs:
            val = kwargs[op]
            if op == 'idVendor':
                self.idVendor = val
            elif op == 'idProduct':
                self.idProduct = val
            elif op == 'iSerial':
                self.iSerial = val
            elif op == 'device':
                self.device = val
            elif op == 'dev':
                self.device = val
            elif op == 'term_char':
                self.term_char = val
            elif op == 'resource':
                resource = val

        if resource is not None:
            res = parse_visa_resource_string(resource)
            if res is None:
                raise UsbtmcException('Invalid resource string', 'init')
            if res['arg1'] is None and res['arg2'] is None:
                raise UsbtmcException('Invalid resource string', 'init')
            self.idVendor = int(res['arg1'], 0)
            self.idProduct = int(res['arg2'], 0)
            self.iSerial = res['arg3']
        if self.device is None:
            if self.idVendor is None or self.idProduct is None:
                raise UsbtmcException('No device specified', 'init')
            else:
                self.device = find_device(self.idVendor, self.idProduct, self.iSerial)
                if self.device is None:
                    raise UsbtmcException('Device not found', 'init')
        return

    def __del__(self):
        if self.connected:
            self.close()

    def open(self):
        if self.connected:
            return
        else:
            for cfg in self.device:
                for iface in cfg:
                    if self.device.idVendor == 4916 or iface.bInterfaceClass == USBTMC_bInterfaceClass and iface.bInterfaceSubClass == USBTMC_bInterfaceSubClass:
                        self.cfg = cfg
                        self.iface = iface
                        break
                    else:
                        continue

                break

            if self.iface is None:
                raise UsbtmcException('Not a USBTMC device', 'init')
            try:
                self.old_cfg = self.device.get_active_configuration()
            except usb.core.USBError:
                pass

            if self.old_cfg is not None and self.old_cfg.bConfigurationValue == self.cfg.bConfigurationValue:
                self._release_kernel_driver(self.iface.bInterfaceNumber)
            else:
                if self.old_cfg is not None:
                    for iface in self.old_cfg:
                        self._release_kernel_driver(iface.bInterfaceNumber)

                self.device.set_configuration(self.cfg)
            usb.util.claim_interface(self.device, self.iface)
            for ep in self.iface:
                ep_dir = usb.util.endpoint_direction(ep.bEndpointAddress)
                ep_type = usb.util.endpoint_type(ep.bmAttributes)
                if ep_type == usb.util.ENDPOINT_TYPE_BULK:
                    if ep_dir == usb.util.ENDPOINT_IN:
                        self.bulk_in_ep = ep
                    elif ep_dir == usb.util.ENDPOINT_OUT:
                        self.bulk_out_ep = ep
                elif ep_type == usb.util.ENDPOINT_TYPE_INTR:
                    if ep_dir == usb.util.ENDPOINT_IN:
                        self.interrupt_in_ep = ep

            if self.bulk_in_ep is None or self.bulk_out_ep is None:
                raise UsbtmcException('Invalid endpoint configuration', 'init')
            if self.device.idVendor == 4916:
                self.max_transfer_size = 63
                self.advantest_quirk = True
            if self.device.idVendor == 6833 and self.device.idProduct in RIGOL_QUIRK_PIDS:
                self.rigol_quirk = True
                if self.device.idProduct == 1230:
                    self.rigol_quirk_ieee_block = True
            self.connected = True
            self.clear()
            self.get_capabilities()
            return

    def close(self):
        if not self.connected:
            return
        usb.util.dispose_resources(self.device)
        try:
            if self.cfg.bConfigurationValue != self.old_cfg.bConfigurationValue:
                self.device.set_configuration(self.old_cfg)
            for iface in self.reattach:
                try:
                    self.device.attach_kernel_driver(iface)
                except:
                    pass

        except:
            pass

        self.reattach = []
        self.connected = False

    def is_usb488(self):
        return self.iface.bInterfaceProtocol == USB488_bInterfaceProtocol

    def get_capabilities(self):
        if not self.connected:
            self.open()
        b = self.device.ctrl_transfer(usb.util.build_request_type(usb.util.CTRL_IN, usb.util.CTRL_TYPE_CLASS, usb.util.CTRL_RECIPIENT_INTERFACE), USBTMC_REQUEST_GET_CAPABILITIES, 0, self.iface.index, 24, timeout=int(self.timeout * 1000))
        if b[0] == USBTMC_STATUS_SUCCESS:
            self.bcdUSBTMC = (b[3] << 8) + b[2]
            self.support_pulse = b[4] & 4 != 0
            self.support_talk_only = b[4] & 2 != 0
            self.support_listen_only = b[4] & 1 != 0
            self.support_term_char = b[5] & 1 != 0
            if self.is_usb488():
                self.bcdUSB488 = (b[13] << 8) + b[12]
                self.support_USB4882 = b[4] & 4 != 0
                self.support_remote_local = b[4] & 2 != 0
                self.support_trigger = b[4] & 1 != 0
                self.support_scpi = b[4] & 8 != 0
                self.support_SR = b[4] & 4 != 0
                self.support_RL = b[4] & 2 != 0
                self.support_DT = b[4] & 1 != 0
        else:
            raise UsbtmcException('Get capabilities failed', 'get_capabilities')

    def pulse(self):
        """
        Send a pulse indicator request, this should blink a light
        for 500-1000ms and then turn off again. (Only if supported)
        """
        if not self.connected:
            self.open()
        if self.support_pulse:
            b = self.device.ctrl_transfer(usb.util.build_request_type(usb.util.CTRL_IN, usb.util.CTRL_TYPE_CLASS, usb.util.CTRL_RECIPIENT_INTERFACE), USBTMC_REQUEST_INDICATOR_PULSE, 0, self.iface.index, 1, timeout=int(self.timeout * 1000))
            if b[0] != USBTMC_STATUS_SUCCESS:
                raise UsbtmcException('Pulse failed', 'pulse')

    def pack_bulk_out_header(self, msgid):
        self.last_btag = btag = self.last_btag % 255 + 1
        return struct.pack('BBBx', msgid, btag, ~btag & 255)

    def pack_dev_dep_msg_out_header(self, transfer_size, eom=True):
        hdr = self.pack_bulk_out_header(USBTMC_MSGID_DEV_DEP_MSG_OUT)
        return hdr + struct.pack('<LBxxx', transfer_size, eom)

    def pack_dev_dep_msg_in_header(self, transfer_size, term_char=None):
        hdr = self.pack_bulk_out_header(USBTMC_MSGID_DEV_DEP_MSG_IN)
        transfer_attributes = 0
        if term_char is None:
            term_char = 0
        else:
            transfer_attributes = 2
            term_char = self.term_char
        return hdr + struct.pack('<LBBxx', transfer_size, transfer_attributes, term_char)

    def pack_vendor_specific_out_header(self, transfer_size):
        hdr = self.pack_bulk_out_header(USBTMC_MSGID_VENDOR_SPECIFIC_OUT)
        return hdr + struct.pack('<Lxxxx', transfer_size)

    def pack_vendor_specific_in_header(self, transfer_size):
        hdr = self.pack_bulk_out_header(USBTMC_MSGID_VENDOR_SPECIFIC_IN)
        return hdr + struct.pack('<Lxxxx', transfer_size)

    def pack_usb488_trigger(self):
        hdr = self.pack_bulk_out_header(USB488_MSGID_TRIGGER)
        return hdr + '\x00\x00\x00\x00\x00\x00\x00\x00'

    def unpack_bulk_in_header(self, data):
        msgid, btag, btaginverse = struct.unpack_from('BBBx', data)
        return (msgid, btag, btaginverse)

    def unpack_dev_dep_resp_header(self, data):
        msgid, btag, btaginverse = self.unpack_bulk_in_header(data)
        transfer_size, transfer_attributes = struct.unpack_from('<LBxxx', data, 4)
        data = data[USBTMC_HEADER_SIZE:transfer_size + USBTMC_HEADER_SIZE]
        return (msgid, btag, btaginverse, transfer_size, transfer_attributes, data)

    def write_raw(self, data):
        """Write binary data to instrument"""
        if not self.connected:
            self.open()
        eom = False
        num = len(data)
        offset = 0
        try:
            while num > 0:
                if num <= self.max_transfer_size:
                    eom = True
                block = data[offset:offset + self.max_transfer_size]
                size = len(block)
                req = self.pack_dev_dep_msg_out_header(size, eom) + block + '\x00' * ((4 - size % 4) % 4)
                self.bulk_out_ep.write(req, timeout=int(self.timeout * 1000))
                offset += size
                num -= size

        except usb.core.USBError:
            exc = sys.exc_info()[1]
            if exc.errno == 110:
                self._abort_bulk_out()
            raise

    def read_raw(self, num=-1):
        """Read binary data from instrument"""
        if not self.connected:
            self.open()
        read_len = self.max_transfer_size
        if 0 < num < read_len:
            read_len = num
        eom = False
        term_char = None
        if self.term_char is not None:
            term_char = self.term_char
        read_data = ''
        try:
            while not eom:
                if not self.rigol_quirk or read_data == '':
                    req = self.pack_dev_dep_msg_in_header(read_len, term_char)
                    self.bulk_out_ep.write(req, timeout=int(self.timeout * 1000))
                resp = self.bulk_in_ep.read(read_len + USBTMC_HEADER_SIZE + 3, timeout=int(self.timeout * 1000))
                if sys.version_info >= (3, 2):
                    resp = resp.tobytes()
                else:
                    resp = resp.tostring()
                if self.rigol_quirk and read_data:
                    pass
                else:
                    msgid, btag, btaginverse, transfer_size, transfer_attributes, data = self.unpack_dev_dep_resp_header(resp)
                if self.rigol_quirk:
                    if read_data:
                        read_data += resp
                    else:
                        if self.rigol_quirk_ieee_block and data.startswith('#'):
                            l = int(chr(data[1]))
                            n = int(data[2:l + 2])
                            transfer_size = n + (l + 2)
                        read_data += data
                    if len(read_data) >= transfer_size:
                        read_data = read_data[:transfer_size]
                        eom = True
                    else:
                        eom = False
                else:
                    eom = transfer_attributes & 1
                    read_data += data
                if self.advantest_quirk:
                    break
                if num > 0:
                    num = num - len(data)
                    if num <= 0:
                        break
                    if num < read_len:
                        read_len = num

        except usb.core.USBError:
            exc = sys.exc_info()[1]
            if exc.errno == 110:
                self._abort_bulk_in()
            raise

        return read_data

    def ask_raw(self, data, num=-1):
        """Write then read binary data"""
        was_locked = self.advantest_locked
        try:
            if self.advantest_quirk and not was_locked:
                self.lock()
            self.write_raw(data)
            return self.read_raw(num)
        finally:
            if self.advantest_quirk and not was_locked:
                self.unlock()

    def write(self, message, encoding='utf-8'):
        """Write string to instrument"""
        if type(message) is tuple or type(message) is list:
            for message_i in message:
                self.write(message_i, encoding)

            return
        self.write_raw(str(message).encode(encoding))

    def read(self, num=-1, encoding='utf-8'):
        """Read string from instrument"""
        return self.read_raw(num).decode(encoding).rstrip('\r\n')

    def ask(self, message, num=-1, encoding='utf-8'):
        """Write then read string"""
        if type(message) is tuple or type(message) is list:
            val = list()
            for message_i in message:
                val.append(self.ask(message_i, num, encoding))

            return val
        was_locked = self.advantest_locked
        try:
            if self.advantest_quirk and not was_locked:
                self.lock()
            self.write(message, encoding)
            return self.read(num, encoding)
        finally:
            if self.advantest_quirk and not was_locked:
                self.unlock()

    def read_stb(self):
        """Read status byte"""
        if not self.connected:
            self.open()
        if self.is_usb488():
            rstb_btag = self.last_rstb_btag % 128 + 1
            if rstb_btag < 2:
                rstb_btag = 2
            self.last_rstb_btag = rstb_btag
            b = self.device.ctrl_transfer(usb.util.build_request_type(usb.util.CTRL_IN, usb.util.CTRL_TYPE_CLASS, usb.util.CTRL_RECIPIENT_INTERFACE), USB488_READ_STATUS_BYTE, rstb_btag, self.iface.index, 3, timeout=int(self.timeout * 1000))
            if b[0] == USBTMC_STATUS_SUCCESS:
                if rstb_btag != b[1]:
                    raise UsbtmcException('Read status byte btag mismatch', 'read_stb')
                if self.interrupt_in_ep is None:
                    return b[2]
                resp = self.interrupt_in_ep.read(2, timeout=int(self.timeout * 1000))
                if resp[0] != rstb_btag + 128:
                    raise UsbtmcException('Read status byte btag mismatch', 'read_stb')
                else:
                    return resp[1]
            else:
                raise UsbtmcException('Read status failed', 'read_stb')
        else:
            return int(self.ask('*STB?'))
        return

    def trigger(self):
        """Send trigger command"""
        if not self.connected:
            self.open()
        if self.support_trigger:
            data = self.pack_usb488_trigger()
            print repr(data)
            self.bulk_out_ep.write(data, timeout=int(self.timeout * 1000))
        else:
            self.write('*TRG')

    def clear(self):
        """Send clear command"""
        if not self.connected:
            self.open()
        b = self.device.ctrl_transfer(usb.util.build_request_type(usb.util.CTRL_IN, usb.util.CTRL_TYPE_CLASS, usb.util.CTRL_RECIPIENT_INTERFACE), USBTMC_REQUEST_INITIATE_CLEAR, 0, self.iface.index, 1, timeout=int(self.timeout * 1000))
        if b[0] == USBTMC_STATUS_SUCCESS:
            while True:
                b = self.device.ctrl_transfer(usb.util.build_request_type(usb.util.CTRL_IN, usb.util.CTRL_TYPE_CLASS, usb.util.CTRL_RECIPIENT_INTERFACE), USBTMC_REQUEST_CHECK_CLEAR_STATUS, 0, self.iface.index, 2, timeout=int(self.timeout * 1000))
                if b[0] == USBTMC_STATUS_PENDING:
                    time.sleep(0.1)
                else:
                    break

            self.bulk_out_ep.clear_halt()
        else:
            raise UsbtmcException('Clear failed', 'clear')

    def _abort_bulk_out(self, btag=None):
        """Abort bulk out"""
        if not self.connected:
            return
        else:
            if btag is None:
                btag = self.last_btag
            b = self.device.ctrl_transfer(usb.util.build_request_type(usb.util.CTRL_IN, usb.util.CTRL_TYPE_CLASS, usb.util.CTRL_RECIPIENT_ENDPOINT), USBTMC_REQUEST_INITIATE_ABORT_BULK_OUT, btag, self.bulk_out_ep.bEndpointAddress, 2, timeout=int(self.timeout * 1000))
            if b[0] == USBTMC_STATUS_SUCCESS:
                while True:
                    b = self.device.ctrl_transfer(usb.util.build_request_type(usb.util.CTRL_IN, usb.util.CTRL_TYPE_CLASS, usb.util.CTRL_RECIPIENT_ENDPOINT), USBTMC_REQUEST_CHECK_ABORT_BULK_OUT_STATUS, 0, self.bulk_out_ep.bEndpointAddress, 8, timeout=int(self.timeout * 1000))
                    if b[0] == USBTMC_STATUS_PENDING:
                        time.sleep(0.1)
                    else:
                        break

            return

    def _abort_bulk_in(self, btag=None):
        """Abort bulk in"""
        if not self.connected:
            return
        else:
            if btag is None:
                btag = self.last_btag
            b = self.device.ctrl_transfer(usb.util.build_request_type(usb.util.CTRL_IN, usb.util.CTRL_TYPE_CLASS, usb.util.CTRL_RECIPIENT_ENDPOINT), USBTMC_REQUEST_INITIATE_ABORT_BULK_IN, btag, self.bulk_in_ep.bEndpointAddress, 2, timeout=int(self.timeout * 1000))
            if b[0] == USBTMC_STATUS_SUCCESS:
                while True:
                    b = self.device.ctrl_transfer(usb.util.build_request_type(usb.util.CTRL_IN, usb.util.CTRL_TYPE_CLASS, usb.util.CTRL_RECIPIENT_ENDPOINT), USBTMC_REQUEST_CHECK_ABORT_BULK_IN_STATUS, 0, self.bulk_in_ep.bEndpointAddress, 8, timeout=int(self.timeout * 1000))
                    if b[0] == USBTMC_STATUS_PENDING:
                        time.sleep(0.1)
                    else:
                        break

            return

    def remote(self):
        """Send remote command"""
        raise NotImplementedError()

    def local(self):
        """Send local command"""
        raise NotImplementedError()

    def lock(self):
        """Send lock command"""
        if not self.connected:
            self.open()
        if self.advantest_quirk:
            self.advantest_locked = True
            self.device.ctrl_transfer(bmRequestType=161, bRequest=160, wValue=1, wIndex=0, data_or_wLength=1)
        else:
            raise NotImplementedError()

    def unlock(self):
        """Send unlock command"""
        if not self.connected:
            self.open()
        if self.advantest_quirk:
            self.advantest_locked = False
            self.device.ctrl_transfer(bmRequestType=161, bRequest=160, wValue=0, wIndex=0, data_or_wLength=1)
        else:
            raise NotImplementedError()

    def advantest_read_myid(self):
        if not self.connected:
            self.open()
        if self.advantest_quirk:
            try:
                return int(self.device.ctrl_transfer(bmRequestType=193, bRequest=245, wValue=0, wIndex=0, data_or_wLength=1)[0])
            except:
                return

        else:
            raise NotImplementedError()
        return

    def _release_kernel_driver(self, interface_number):
        if os.name == 'posix':
            if self.device.is_kernel_driver_active(interface_number):
                self.reattach.append(interface_number)
                try:
                    self.device.detach_kernel_driver(interface_number)
                except usb.core.USBError as e:
                    sys.exit(('Could not detach kernel driver from interface({0}): {1}').format(interface_number, str(e)))