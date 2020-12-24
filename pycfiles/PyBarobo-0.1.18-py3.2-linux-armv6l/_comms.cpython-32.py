# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv6l/egg/barobo/_comms.py
# Compiled at: 2014-09-16 14:39:13
import socket
try:
    import serial
    havePySerial = True
except:
    havePySerial = False

import threading, struct, time, barobo, ctypes, ctypes.util, os, sys
haveSFP = False
try:
    from sys import platform
    if 'win32' == platform:
        for p in sys.path:
            fname = os.path.join(p, 'barobo/lib/libsfp.dll')
            if os.path.isfile(fname):
                _sfp = ctypes.CDLL(fname)
                haveSFP = True
                break

    else:
        for p in sys.path:
            fname = os.path.join(p, 'barobo/lib/libsfp.so')
            if os.path.isfile(fname):
                _sfp = ctypes.CDLL(fname)
                haveSFP = True
                break

    _SFP_WRITE_MULTIPLE = 1
except:
    haveSFP = False

DEBUG = False

class Packet:

    def __init__(self, data=None, addr=None):
        self.data = data
        self.addr = addr

    def __getitem__(self, key):
        return self.data[key]

    def __len__(self):
        return len(self.data)


if havePySerial:

    class PhysicalLayer_TTY(serial.Serial):

        def __init__(self, ttyfilename):
            serial.Serial.__init__(self, ttyfilename, baudrate=230400)
            time.sleep(1)
            self.stopbits = serial.STOPBITS_TWO
            self.timeout = None
            return

        def disconnect(self):
            self.close()


class PhysicalLayer_Socket(socket.socket):

    def __init__(self, hostname, port):
        socket.socket.__init__(self)
        self.connect((hostname, port))

    def disconnect(self):
        self.close()

    def flush(self):
        pass

    def flushInput(self):
        pass

    def flushOutput(self):
        pass

    def read(self):
        return self.recv(1)

    def write(self, packet):
        self.sendall(packet)


import sys
if sys.version_info[0] >= 3 and sys.version_info[1] >= 3:
    import socket

    class PhysicalLayer_Bluetooth:

        def __init__(self, bluetooth_mac_addr):
            self.sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
            self.sock.connect((bluetooth_mac_addr, 1))

        def disconnect(self):
            self.sock.close()

        def flush(self):
            pass

        def flushInput(self):
            pass

        def flushOutput(self):
            pass

        def read(self):
            return self.sock.recv(1)

        def write(self, packet):
            self.sock.sendall(packet)


else:
    try:
        import bluetooth

        class PhysicalLayer_Bluetooth(bluetooth.BluetoothSocket):

            def __init__(self, bluetooth_mac_addr):
                bluetooth.BluetoothSocket.__init__(self, bluetooth.RFCOMM)
                self.connect((bluetooth_mac_addr, 1))

            def disconnect(self):
                self.close()

            def flush(self):
                pass

            def flushInput(self):
                pass

            def flushOutput(self):
                pass

            def read(self):
                return self.recv(1)

            def write(self, packet):
                import os
                if os.name == 'nt':
                    self.send(str(packet))
                else:
                    self.sendall(str(bytearray(packet)))


    except:
        pass

class LinkLayer_Base:

    def __init__(self, physicalLayer, readCallback):
        self.phys = physicalLayer
        self.deliver = readCallback
        self.writeLock = threading.Lock()
        self.stopflag = False

    def start(self):
        self.thread = threading.Thread(target=self._run)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        self.stopflag = True


class LinkLayer_TTY(LinkLayer_Base):

    def __init__(self, physicalLayer, readCallback):
        LinkLayer_Base.__init__(self, physicalLayer, readCallback)

    def write(self, packet, address):
        newpacket = bytearray([packet[0],
         len(packet) + 5,
         address >> 8,
         address & 255,
         1])
        newpacket += bytearray(packet)
        self.writeLock.acquire()
        if DEBUG:
            print('Send: {0}'.format(list(map(hex, newpacket))))
        self.phys.write(newpacket)
        self.writeLock.release()

    def _run(self):
        self.readbuf = bytearray([])
        self.phys.flush()
        self.phys.flushInput()
        self.phys.flushOutput()
        while 1:
            byte = self.phys.read()
            if self.stopflag:
                break
            if byte is None:
                continue
            if DEBUG:
                print('Byte: {0}'.format(list(map(hex, bytearray(byte)))))
            self.readbuf += bytearray(byte)
            if len(self.readbuf) <= 2:
                continue
            if len(self.readbuf) == self.readbuf[1]:
                if DEBUG:
                    print('Recv: {0}'.format(list(map(hex, self.readbuf))))
                zigbeeAddr = barobo._unpack('!H', self.readbuf[2:4])[0]
                if self.readbuf[0] != barobo.BaroboCtx.EVENT_REPORTADDRESS:
                    pkt = Packet(self.readbuf[5:-1], zigbeeAddr)
                else:
                    pkt = Packet(self.readbuf, zigbeeAddr)
                self.deliver(pkt)
                self.readbuf = self.readbuf[self.readbuf[1]:]
                continue

        return


class LinkLayer_SFP(LinkLayer_Base):

    def __init__(self, physicalLayer, readCallback):
        LinkLayer_Base.__init__(self, physicalLayer, readCallback)
        self.ctx = (ctypes.c_ubyte * _sfp.sfpGetSizeof())()
        _sfp.sfpInit(self.ctx)
        self.SFPdeliverfun = ctypes.CFUNCTYPE(None, ctypes.POINTER(ctypes.c_ubyte), ctypes.c_ulong, ctypes.c_void_p)
        self.SFPwritenfun = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.POINTER(ctypes.c_ubyte), ctypes.c_ulong, ctypes.POINTER(ctypes.c_ulong), ctypes.c_void_p)
        self.SFPlockfun = ctypes.CFUNCTYPE(None, ctypes.c_void_p)
        self.SFPunlockfun = ctypes.CFUNCTYPE(None, ctypes.c_void_p)
        self.sfp_deliver_cb = self.SFPdeliverfun(self.sfp_deliver)
        self.sfp_write_cb = self.SFPwritenfun(self.sfp_write)
        self.sfp_lock_tx_cb = self.SFPlockfun(self.sfp_lock_tx)
        self.sfp_unlock_tx_cb = self.SFPunlockfun(self.sfp_unlock_tx)
        _sfp.sfpSetDeliverCallback(self.ctx, self.sfp_deliver_cb, None)
        _sfp.sfpSetWriteCallback(self.ctx, _SFP_WRITE_MULTIPLE, self.sfp_write_cb, None)
        _sfp.sfpSetLockCallback(self.ctx, self.sfp_lock_tx_cb, None)
        _sfp.sfpSetUnlockCallback(self.ctx, self.sfp_unlock_tx_cb, None)
        return

    def sfp_deliver(self, buf, size, userdata):
        if size <= 2:
            return
        if size == buf[1]:
            if DEBUG:
                print('Recv: {0}'.format(list(map(hex, buf[:size]))))
            zigbeeAddr = barobo._unpack('!H', bytearray(buf[2:4]))[0]
            if buf[0] != barobo.BaroboCtx.EVENT_REPORTADDRESS:
                pkt = Packet(bytearray(buf[5:size]), zigbeeAddr)
            else:
                pkt = Packet(bytearray(buf[:size]), zigbeeAddr)
            self.deliver(pkt)

    def sfp_write(self, buf, size, outlen, userdata):
        if DEBUG:
            print('Send: {0}'.format(list(map(hex, buf[:size]))))
        outlen_w = ctypes.cast(outlen, ctypes.POINTER(ctypes.c_ulong))
        addr = ctypes.addressof(outlen_w.contents)
        outlen_w2 = ctypes.c_ulong.from_address(addr)
        outlen_w2 = self.phys.write(bytearray(buf[:size]))
        return 0

    def sfp_lock_tx(self, userdata):
        self.writeLock.acquire()

    def sfp_unlock_tx(self, userdata):
        self.writeLock.release()

    def write(self, packet, address):
        newpacket = bytearray([packet[0],
         len(packet) + 5,
         address >> 8,
         address & 255,
         1])
        newpacket += bytearray(packet)
        buf = (ctypes.c_ubyte * len(newpacket))(*newpacket)
        _sfp.sfpWritePacket(self.ctx, buf, len(buf), None)
        return

    def _run(self):
        self.phys.flush()
        self.phys.flushInput()
        self.phys.flushOutput()
        _sfp.sfpConnect(self.ctx)
        while True:
            byte = self.phys.read()
            if self.stopflag:
                break
            if byte is None:
                continue
            if DEBUG:
                print('Byte: {0}'.format(list(map(hex, bytearray(byte)))))
            from sys import version_info
            if version_info < (3, 0):
                octet = ord(byte[0])
            else:
                octet = byte[0]
            rc = _sfp.sfpDeliverOctet(self.ctx, octet, None, 0, None)

        if DEBUG:
            print('SFP Link Layer stopping...')
        return


class LinkLayer_Socket(LinkLayer_Base):

    def __init__(self, physicalLayer, readCallback):
        LinkLayer_Base.__init__(self, physicalLayer, readCallback)

    def write(self, packet, address):
        self.writeLock.acquire()
        self.phys.write(packet)
        if DEBUG:
            print('Send: {0}'.format(list(map(hex, packet))))
        self.writeLock.release()

    def _run(self):
        self.readbuf = bytearray([])
        self.phys.flush()
        self.phys.flushInput()
        self.phys.flushOutput()
        while 1:
            byte = self.phys.read()
            if self.stopflag:
                break
            if DEBUG:
                print('Byte: {0}'.format(list(map(hex, bytearray(byte)))))
            if byte is None:
                continue
            self.readbuf += bytearray(byte)
            if len(self.readbuf) <= 2:
                continue
            if len(self.readbuf) == self.readbuf[1]:
                if DEBUG:
                    print('Recv: {0}'.format(list(map(hex, self.readbuf))))
                pkt = Packet(self.readbuf, 32768)
                self.deliver(pkt)
                self.readbuf = self.readbuf[self.readbuf[1]:]
                continue

        return