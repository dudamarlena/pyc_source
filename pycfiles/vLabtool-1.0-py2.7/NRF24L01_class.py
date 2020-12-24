# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vLabtool/NRF24L01_class.py
# Compiled at: 2015-07-21 16:38:12
from commands_proto import *
import time

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
    ADC_COMMANDS = 1
    READ_ADC = 0
    I2C_COMMANDS = 2
    I2C_TRANSACTION = 0
    I2C_WRITE = 16
    SCAN_I2C = 32
    PULL_SCL_LOW = 48
    I2C_CONFIG = 64
    I2C_READ = 80
    NRF_COMMANDS = 3
    NRF_READ_REGISTER = 0
    NRF_WRITE_REGISTER = 16
    CURRENT_ADDRESS = 11184641
    nodelist = {}
    nodepos = 0
    NODELIST_MAXLENGTH = 15

    def __init__(self, H):
        self.H = H
        self.init()
        self.selectAddress(self.CURRENT_ADDRESS)
        self.rxmode()
        time.sleep(0.1)
        self.flush()

    def init(self):
        self.H.__sendByte__(NRFL01)
        self.H.__sendByte__(NRF_SETUP)
        self.H.__get_ack__()
        time.sleep(0.015)

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

    def triggerAll(self, val):
        self.txmode()
        self.selectAddress(1118481)
        self.write_register(self.EN_AA, 0)
        self.write_payload([val], True)
        self.write_register(self.EN_AA, 1)

    def power_down(self):
        self.H.__sendByte__(NRFL01)
        self.H.__sendByte__(NRF_POWER_DOWN)
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
        print 'writing', address, value
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

    def selectAddress(self, address):
        self.H.__sendByte__(NRFL01)
        self.H.__sendByte__(NRF_WRITEADDRESSES)
        self.H.__sendByte__(address & 255)
        self.H.__sendByte__(address >> 8 & 255)
        self.H.__sendByte__(address >> 16 & 255)
        self.H.__get_ack__()
        self.CURRENT_ADDRESS = address

    def read_payload(self, numbytes):
        self.H.__sendByte__(NRFL01)
        self.H.__sendByte__(NRF_READPAYLOAD)
        self.H.__sendByte__(numbytes)
        data = self.H.fd.read(numbytes)
        self.H.__get_ack__()
        return [ ord(a) for a in data ]

    def write_payload(self, data, verbose=False, **args):
        self.H.__sendByte__(NRFL01)
        self.H.__sendByte__(NRF_WRITEPAYLOAD)
        numbytes = len(data) | 128
        if args.get('rxmode', False):
            numbytes |= 64
        self.H.__sendByte__(numbytes)
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

    def I2C_scan(self):
        import sensorlist
        print 'Scanning addresses 0-127...'
        x = self.transaction([self.I2C_COMMANDS | self.I2C_SCAN | 128], timeout=500)
        if not x:
            return []
        if not sum(x):
            return []
        addrs = []
        print 'Address', '\t', 'Possible Devices'
        for a in range(16):
            if x[a] ^ 255:
                for b in range(8):
                    if x[a] & 128 >> b == 0:
                        addr = 8 * a + b
                        addrs.append(addr)
                        print hex(addr), '\t\t', sensorlist.sensors.get(addr, 'None')

        return addrs

    def transaction(self, data, **args):
        self.H.__sendByte__(NRFL01)
        self.H.__sendByte__(NRF_TRANSACTION)
        self.H.__sendByte__(len(data))
        if not args.has_key('listen'):
            args['listen'] = True
        if args.get('listen', False):
            data[0] |= 128
        timeout = args.get('timeout', 200)
        verbose = args.get('verbose', False)
        self.H.__sendInt__(timeout)
        for a in data:
            self.H.__sendByte__(a)

        numbytes = self.H.__getByte__()
        if numbytes:
            data = self.H.fd.read(numbytes)
        else:
            data = []
        val = self.H.__get_ack__() >> 4
        if verbose:
            if val & 1:
                print time.time(), '%s Err. Node not found' % hex(self.CURRENT_ADDRESS)
            if val & 2:
                print time.time(), '%s Err. NRF on-board transmitter not found' % hex(self.CURRENT_ADDRESS)
            if val & 4 and args['listen']:
                print time.time(), '%s Err. Node received command but did not reply' % hex(self.CURRENT_ADDRESS)
        if val & 7:
            self.flush()
            return False
        return [ ord(a) for a in data ]

    def transactionWithRetries(self, data, **args):
        retries = args.get('retries', 5)
        reply = False
        while retries > 0:
            reply = self.transaction(data, verbose=(retries == 1), **args)
            if reply:
                break
            retries -= 1

        return reply

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

    def start_token_manager(self):
        """
                """
        self.H.__sendByte__(NRFL01)
        self.H.__sendByte__(NRF_START_TOKEN_MANAGER)
        self.H.__get_ack__()

    def stop_token_manager(self):
        """
                """
        self.H.__sendByte__(NRFL01)
        self.H.__sendByte__(NRF_STOP_TOKEN_MANAGER)
        self.H.__get_ack__()

    def total_tokens(self):
        """
                """
        self.H.__sendByte__(NRFL01)
        self.H.__sendByte__(NRF_TOTAL_TOKENS)
        x = self.H.__getByte__()
        self.H.__get_ack__()
        return x

    def fetch_report(self, num):
        """
                """
        self.H.__sendByte__(NRFL01)
        self.H.__sendByte__(NRF_REPORTS)
        self.H.__sendByte__(num)
        data = [ self.H.__getByte__() for a in range(20) ]
        self.H.__get_ack__()
        return data

    def __decode_I2C_list__(self, data):
        lst = []
        if sum(data) == 0:
            return lst
        for a in range(len(data)):
            if data[a] ^ 255:
                for b in range(8):
                    if data[a] & 128 >> b == 0:
                        addr = 8 * a + b
                        lst.append(addr)

        return lst

    def get_nodelist(self):
        """
                Refer to the variable 'nodelist' if you simply want a list of nodes that either registered while your code was
                running , or were loaded from the firmware buffer(max 15 entries)

                If you plan to use more than 15 nodes, and wish to register their addresses without having to feed them manually,
                then this function must be called each time before the buffer resets.
                
                The dictionary object returned by this function [addresses paired with arrays containing their registered sensors]
                is filtered by checking with each node if they are alive.
                
                """
        total = self.total_tokens()
        if self.nodepos != total:
            for nm in range(self.NODELIST_MAXLENGTH):
                dat = self.fetch_report(nm)
                txrx = dat[0] | dat[1] << 8 | dat[2] << 16
                if not txrx:
                    continue
                self.nodelist[txrx] = self.__decode_I2C_list__(dat[3:19])
                self.nodepos = total

        filtered_lst = {}
        for a in self.nodelist:
            if self.isAlive(a):
                filtered_lst[a] = self.nodelist[a]

        return filtered_lst

    def __delete_registered_node__(self, num):
        self.H.__sendByte__(NRFL01)
        self.H.__sendByte__(NRF_DELETE_REPORT_ROW)
        self.H.__sendByte__(num)
        self.H.__get_ack__()

    def __delete_all_registered_nodes__(self):
        while self.total_tokens():
            print '-'
            self.__delete_registered_node__(0)

    def isAlive(self, addr):
        self.selectAddress(addr)
        return self.transaction([self.NRF_COMMANDS | self.NRF_READ_REGISTER] + [self.R_STATUS], timeout=100, verbose=False)

    def init_shockburst_transmitter(self, **args):
        """
                Puts the radio into transmit mode.
                Dynamic Payload with auto acknowledge is enabled.
                upto 5 retransmits with 1ms delay between each in case a node doesn't respond in time
                Receivers must acknowledge payloads
                """
        self.PAYLOAD_SIZE = args.get('PAYLOAD_SIZE', self.PAYLOAD_SIZE)
        myaddr = args.get('myaddr', 11184641)
        sendaddr = args.get('sendaddr', 11184641)
        self.init()
        self.write_address(self.RX_ADDR_P0, myaddr)
        self.write_address(self.TX_ADDR, sendaddr)
        self.write_register(self.RX_PW_P0, self.PAYLOAD_SIZE)
        self.rxmode()
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