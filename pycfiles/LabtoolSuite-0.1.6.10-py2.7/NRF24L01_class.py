# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Labtools/NRF24L01_class.py
# Compiled at: 2015-06-14 00:55:30
from commands_proto import *

class NRF24L01:
    R_REG = 0
    W_REG = 32
    RX_PAYLOAD = 97
    TX_PAYLOAD = 160
    ACK_PAYLOAD = 168
    FLUSH_TX = 225
    FLUSH_RX = 226
    ACTIVATE = 80
    R_STATUS = 255
    NRF_CONFIG = 0
    EN_AA = 1
    EN_RXADDR = 2
    SETUP_AW = 3
    SETUP_RETR = 4
    RF_CH = 5
    RF_SETUP = 6
    NRF_STATUS = 7
    OBSERVE_TX = 8
    CD = 9
    RX_ADDR_P0 = 10
    RX_ADDR_P1 = 11
    RX_ADDR_P2 = 12
    RX_ADDR_P3 = 13
    RX_ADDR_P4 = 14
    RX_ADDR_P5 = 15
    TX_ADDR = 16
    RX_PW_P0 = 17
    RX_PW_P1 = 18
    RX_PW_P2 = 19
    RX_PW_P3 = 20
    RX_PW_P4 = 21
    RX_PW_P5 = 22
    R_RX_PL_WID = 96
    FIFO_STATUS = 23
    DYNPD = 28
    FEATURE = 29
    PAYLOAD_SIZE = 0
    ACK_PAYLOAD_SIZE = 0
    READ_PAYLOAD_SIZE = 0

    def __init__(self, H):
        self.H = H

    def init(self):
        self.H.__sendByte__(NRFL01)
        self.H.__sendByte__(NRF_SETUP)
        self.H.__get_ack__()
        time.sleep(0.15)

    def rxmode(self):
        """
                Puts the radio into listening mode.
                """
        self.H.__sendByte__(NRFL01)
        self.H.__sendByte__(NRF_RXMODE)
        self.H.__get_ack__()

    def txmode(self):
        """
                Puts the radio into transmit mode.
                """
        self.H.__sendByte__(NRFL01)
        self.H.__sendByte__(NRF_TXMODE)
        self.H.__get_ack__()

    def power_down(self):
        self.H.__sendByte__(NRFL01)
        self.H.__sendByte__(NRF_POWERDOWN)
        self.H.__get_ack__()

    def rxchar(self):
        """
                Receives a 1 Byte payload
                """
        self.H.__sendByte__(NRFL01)
        self.H.__sendByte__(NRF_RXCHAR)
        value = self.H.__getByte__()
        self.H.__get_ack__()
        return value

    def txchar(self, char):
        """
                Transmits a single character
                """
        self.H.__sendByte__(NRFL01)
        self.H.__sendByte__(NRF_TXCHAR)
        self.H.__sendByte__(char)
        return self.H.__get_ack__() >> 4

    def hasData(self):
        """
                Check if the RX FIFO contains data
                """
        self.H.__sendByte__(NRFL01)
        self.H.__sendByte__(NRF_HASDATA)
        value = self.H.__getByte__()
        self.H.__get_ack__()
        return value

    def flush(self):
        """
                Flushes the TX and RX FIFOs
                """
        self.H.__sendByte__(NRFL01)
        self.H.__sendByte__(NRF_FLUSH)
        self.H.__get_ack__()

    def write_register(self, address, value):
        """
                write a  byte to any of the configuration registers on the Radio.
                address byte can either be located in the NRF24L01+ manual, or chosen
                from some of the constants defined in this module.
                """
        self.H.__sendByte__(NRFL01)
        self.H.__sendByte__(NRF_WRITEREG)
        self.H.__sendByte__(address)
        self.H.__sendByte__(value)
        self.H.__get_ack__()

    def read_register(self, address):
        """
                Read the value of any of the configuration registers on the radio module.
                
                """
        self.H.__sendByte__(NRFL01)
        self.H.__sendByte__(NRF_READREG)
        self.H.__sendByte__(address)
        val = self.H.__getByte__()
        self.H.__get_ack__()
        return val

    def get_status(self):
        """
                Returns a byte representing the STATUS register on the radio.
                Refer to NRF24L01+ documentation for further details
                """
        self.H.__sendByte__(NRFL01)
        self.H.__sendByte__(NRF_GETSTATUS)
        val = self.H.__getByte__()
        self.H.__get_ack__()
        return val

    def write_command(self, cmd):
        self.H.__sendByte__(NRFL01)
        self.H.__sendByte__(NRF_WRITECOMMAND)
        self.H.__sendByte__(cmd)
        self.H.__get_ack__()

    def write_address(self, register, address):
        """
                register can be TX_ADDR, RX_ADDR_P0 -> RX_ADDR_P5
                3 byte address.  eg 0xFFABXX . XX cannot be FF
                if RX_ADDR_P1 needs to be used along with any of the pipes
                from P2 to P5, then RX_ADDR_P1 must be updated last.
                Addresses from P1-P5 must share the first two bytes.
                """
        self.H.__sendByte__(NRFL01)
        self.H.__sendByte__(NRF_WRITEADDRESS)
        self.H.__sendByte__(register)
        self.H.__sendByte__(address & 255)
        self.H.__sendByte__(address >> 8 & 255)
        self.H.__sendByte__(address >> 16 & 255)
        self.H.__get_ack__()

    def init_shockburst_transmitter(self, **args):
        """
                Puts the radio into transmit mode.
                Dynamic Payload with auto acknowledge is enabled.
                upto 5 retransmits with 1ms delay between each in case a node doesn't respond in time
                Receivers must acknowledge payloads
                
                """
        self.PAYLOAD_SIZE = args.get('PAYLOAD_SIZE', self.PAYLOAD_SIZE)
        myaddr = args.get('myaddr', 10822581)
        sendaddr = args.get('sendaddr', 10822581)
        self.init()
        self.write_register(self.RF_CH, 10)
        self.write_register(self.RF_SETUP, 38)
        self.write_address(self.TX_ADDR, sendaddr)
        self.write_address(self.RX_ADDR_P0, myaddr)
        self.write_register(self.EN_AA, 1)
        self.write_register(self.DYNPD, 1)
        self.write_register(self.EN_RXADDR, 1)
        self.write_register(self.FEATURE, 4)
        self.write_register(self.SETUP_RETR, 255)
        self.write_register(self.RX_PW_P0, self.PAYLOAD_SIZE)
        self.txmode()
        time.sleep(0.1)
        self.flush()

    def init_shockburst_receiver(self, **args):
        """
                Puts the radio into receive mode.
                Dynamic Payload with auto acknowledge is enabled.
                """
        self.PAYLOAD_SIZE = args.get('PAYLOAD_SIZE', self.PAYLOAD_SIZE)
        if not args.has_key('myaddr0'):
            args['myaddr0'] = 10822581
        print args
        self.init()
        self.write_register(self.RF_CH, 10)
        self.write_register(self.RF_SETUP, 38)
        enabled_pipes = 0
        for a in range(0, 6):
            x = args.get('myaddr' + str(a), None)
            if x:
                print hex(x), hex(self.RX_ADDR_P0 + a)
                enabled_pipes |= 1 << a
                self.write_address(self.RX_ADDR_P0 + a, x)

        P15_base_address = args.get('myaddr1', None)
        if P15_base_address:
            self.write_address(self.RX_ADDR_P1, P15_base_address)
        self.write_register(self.EN_RXADDR, enabled_pipes)
        self.write_register(self.EN_AA, enabled_pipes)
        self.write_register(self.DYNPD, enabled_pipes)
        self.write_register(self.FEATURE, 6)
        self.rxmode()
        time.sleep(0.1)
        self.flush()
        return

    def init_transmitter(self, **args):
        self.PAYLOAD_SIZE = args.get('PAYLOAD_SIZE', self.PAYLOAD_SIZE)
        myaddr = args.get('myaddr', 10822581)
        sendaddr = args.get('sendaddr', 10822581)
        self.init()
        self.write_register(self.RF_CH, 10)
        self.write_register(self.RF_SETUP, 38)
        self.write_address(self.TX_ADDR, sendaddr)
        self.write_address(self.RX_ADDR_P0, myaddr)
        self.write_register(self.EN_AA, 0)
        self.write_register(self.DYNPD, 0)
        self.write_register(self.FEATURE, 0)
        self.write_register(self.SETUP_RETR, 0)
        self.write_register(self.RX_PW_P0, self.PAYLOAD_SIZE)
        self.txmode()
        time.sleep(0.1)
        self.flush()

    def init_receiver(self, **args):
        self.PAYLOAD_SIZE = args.get('PAYLOAD_SIZE', self.PAYLOAD_SIZE)
        myaddr = args.get('myaddr', 10822581)
        sendaddr = args.get('sendaddr', 10822581)
        self.init()
        self.write_register(self.RF_CH, 10)
        self.write_register(self.RF_SETUP, 38)
        self.write_address(self.TX_ADDR, sendaddr)
        self.write_address(self.RX_ADDR_P0, myaddr)
        enabled_pipes = 1
        for a in range(1, 6):
            x = args.get('myaddr' + str(a), None)
            if x:
                print hex(x), hex(self.RX_ADDR_P0 + a)
                enabled_pipes |= 1 << a
                self.write_address(self.RX_ADDR_P0 + a, x)

        P15_base_address = args.get('myaddr1', None)
        if P15_base_address:
            self.write_address(self.RX_ADDR_P1, P15_base_address)
        self.write_register(self.EN_RXADDR, enabled_pipes)
        self.write_register(self.EN_AA, 0)
        self.write_register(self.DYNPD, 0)
        self.write_register(self.FEATURE, 0)
        self.write_register(self.RX_PW_P0, self.PAYLOAD_SIZE)
        self.rxmode()
        time.sleep(0.1)
        self.flush()
        return

    def read_payload(self, numbytes):
        self.H.__sendByte__(NRFL01)
        self.H.__sendByte__(NRF_READPAYLOAD)
        self.H.__sendByte__(numbytes)
        data = self.H.fd.read(numbytes)
        self.H.__get_ack__()
        return [ ord(a) for a in data ]

    def write_payload(self, data, verbose=False):
        self.H.__sendByte__(NRFL01)
        self.H.__sendByte__(NRF_WRITEPAYLOAD)
        self.H.__sendByte__(len(data) | 128)
        self.H.__sendByte__(self.TX_PAYLOAD)
        for a in data:
            self.H.__sendByte__(a)

        val = self.H.__get_ack__() >> 4
        if verbose:
            if val & 2:
                print ' NRF radio not found. Connect one to the add-on port'
            elif val & 1:
                print ' Node probably dead/out of range. It failed to acknowledge'
            return
        return val

    def transaction(self, data, timeout=100, verbose=True):
        self.H.__sendByte__(NRFL01)
        self.H.__sendByte__(NRF_TRANSACTION)
        self.H.__sendByte__(len(data))
        self.H.__sendInt__(timeout)
        for a in data:
            self.H.__sendByte__(a)

        bytes = self.H.__getByte__()
        if bytes:
            data = self.H.fd.read(bytes)
        else:
            data = []
        val = self.H.__get_ack__() >> 4
        if verbose:
            if val & 2:
                print ' NRF radio not found. Connect one to the add-on port'
            if val & 1:
                print ' Node probably dead/out of range. It failed to acknowledge'
            if val & 4:
                print 'Node failed to reply despite having acknowledged the order'
            if val & 7:
                self.flush()
                return
        return [ ord(a) for a in data ]

    def write_ack_payload(self, data, pipe):
        if len(data) != self.ACK_PAYLOAD_SIZE:
            self.ACK_PAYLOAD_SIZE = len(data)
            if self.ACK_PAYLOAD_SIZE > 15:
                print 'too large. truncating.'
                self.ACK_PAYLOAD_SIZE = 15
                data = data[:15]
            else:
                print 'ack payload size:', self.ACK_PAYLOAD_SIZE
        self.H.__sendByte__(NRFL01)
        self.H.__sendByte__(NRF_WRITEPAYLOAD)
        self.H.__sendByte__(len(data))
        self.H.__sendByte__(self.ACK_PAYLOAD | pipe)
        for a in data:
            self.H.__sendByte__(a)

        return self.H.__get_ack__() >> 4