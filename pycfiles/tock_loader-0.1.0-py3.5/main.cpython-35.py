# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/tockloader/main.py
# Compiled at: 2016-12-16 13:50:07
# Size of source mod 2**32: 11377 bytes
import argparse, struct, sys, time, crcmod, serial, serial.tools.list_ports, serial.tools.miniterm
ESCAPE_CHAR = 252
COMMAND_PING = 1
COMMAND_INFO = 3
COMMAND_ID = 4
COMMAND_RESET = 5
COMMAND_ERASE_PAGE = 6
COMMAND_WRITE_PAGE = 7
COMMAND_XEBLOCK = 8
COMMAND_XWPAGE = 9
COMMAND_CRCRX = 16
COMMAND_RRANGE = 17
COMMAND_XRRANGE = 18
COMMAND_SATTR = 19
COMMAND_GATTR = 20
COMMAND_CRC_INTERNAL_FLASH = 21
COMMAND_CRCEF = 22
COMMAND_XEPAGE = 23
COMMAND_XFINIT = 24
COMMAND_CLKOUT = 25
COMMAND_WUSER = 32
RESPONSE_OVERFLOW = 16
RESPONSE_PONG = 17
RESPONSE_BADADDR = 18
RESPONSE_INTERROR = 19
RESPONSE_BADARGS = 20
RESPONSE_OK = 21
RESPONSE_UNKNOWN = 22
RESPONSE_XFTIMEOUT = 23
RESPONSE_XFEPE = 24
RESPONSE_CRCRX = 25
RESPONSE_RRANGE = 32
RESPONSE_XRRANGE = 33
RESPONSE_GATTR = 34
RESPONSE_CRC_INTERNAL_FLASH = 35
RESPONSE_CRCXF = 36
RESPONSE_INFO = 37
SYNC_MESSAGE = bytes([0, ESCAPE_CHAR, COMMAND_RESET])

class TockLoader:

    def open(self, port):
        if port == None:
            print('No serial port specified. Discovering attached serial devices...')
            ports = list(serial.tools.list_ports.comports())
            if len(ports) == 0:
                print('No serial ports found. Is the board connected?')
                return False
            print('Found {} serial port(s).'.format(len(ports)))
            print('Using "{}"'.format(ports[0]))
            port = ports[0][0]
        self.sp = serial.Serial()
        self.sp.port = port
        self.sp.baudrate = 115200
        self.sp.parity = serial.PARITY_NONE
        self.sp.stopbits = 1
        self.sp.xonxoff = 0
        self.sp.rtscts = 0
        self.sp.timeout = 0.5
        self.sp.dtr = 0
        self.sp.rts = 0
        self.sp.open()
        return True

    def enter_bootloader_mode(self):
        self.sp.dtr = 1
        self.sp.rts = 1
        time.sleep(0.1)
        self.sp.dtr = 0
        time.sleep(0.5)
        self.sp.rts = 0

    def exit_bootloader_mode(self):
        self.sp.dtr = 1
        self.sp.rts = 0
        time.sleep(0.1)
        self.sp.dtr = 0

    def ping_bootloader_and_wait_for_response(self):
        for i in range(30):
            ping_pkt = bytes([252, 1])
            self.sp.write(ping_pkt)
            ret = self.sp.read(2)
            if len(ret) == 2 and ret[1] == RESPONSE_PONG:
                return True

        return False

    def flash_binary(self, binary, address):
        self.enter_bootloader_mode()
        alive = self.ping_bootloader_and_wait_for_response()
        if not alive:
            print('Error connecting to bootloader. No "pong" received.')
            print('Things that could be wrong:')
            print('  - The bootloader is not flashed on the chip')
            print('  - The DTR/RTS lines are not working')
            print('  - The serial port being used is incorrect')
            print('  - The bootloader API has changed')
            print('  - There is a bug in this script')
            return False
        if len(binary) % 512 != 0:
            remaining = 512 - len(binary) % 512
            binary += bytes([255] * remaining)
        then = time.time()
        for i in range(len(binary) // 512):
            self.sp.write(SYNC_MESSAGE)
            time.sleep(0.0001)
            pkt = struct.pack('<I', address + i * 512)
            pkt += binary[i * 512:(i + 1) * 512]
            pkt = pkt.replace(bytes([ESCAPE_CHAR]), bytes([ESCAPE_CHAR, ESCAPE_CHAR]))
            pkt += bytes([ESCAPE_CHAR, COMMAND_WRITE_PAGE])
            self.sp.write(pkt)
            ret = self.sp.read(2)
            if ret[0] != ESCAPE_CHAR:
                print('Error: Invalid response from bootloader when flashing page')
                return False
            if ret[1] != RESPONSE_OK:
                print('Error: Error when flashing page')
                if ret[1] == RESPONSE_BADADDR:
                    print('Error: RESPONSE_BADADDR: Invalid address for page to write (address: 0x{:X}'.format(address + i * 512))
                else:
                    if ret[1] == RESPONSE_INTERROR:
                        print('Error: RESPONSE_INTERROR: Internal error when writing flash')
                    else:
                        if ret[1] == RESPONSE_BADARGS:
                            print('Error: RESPONSE_BADARGS: Invalid length for flash page write')
                        else:
                            print('Error: 0x{:X}'.format(ret[1]))
                    return False

        now = time.time()
        print('Wrote {} bytes in {:0.3f} seconds'.format(len(binary), now - then))
        self.sp.write(SYNC_MESSAGE)
        time.sleep(0.0001)
        pkt = struct.pack('<II', address, len(binary)) + bytes([ESCAPE_CHAR, COMMAND_CRC_INTERNAL_FLASH])
        self.sp.write(pkt)
        ret = self.sp.read(6)
        if len(ret) < 2:
            print('Error: No response when requesting the CRC')
            return False
        if ret[0] != ESCAPE_CHAR:
            print('Error: Invalid response from bootloader when asking for CRC')
            return False
        if ret[1] != RESPONSE_CRC_INTERNAL_FLASH:
            print('Error: Error when flashing page')
            if ret[1] == RESPONSE_BADADDR:
                print('Error: RESPONSE_BADADDR: Invalid address for CRC (address: 0x{:X})'.format(address))
        else:
            if ret[1] == RESPONSE_BADARGS:
                print('Error: RESPONSE_BADARGS: Invalid length for CRC check')
            else:
                print('Error: 0x{:X}'.format(ret[1]))
            return False
        crc_bootloader = struct.unpack('<I', ret[2:6])[0]
        crc_function = crcmod.mkCrcFun(4374732215, initCrc=0, xorOut=4294967295)
        crc_loader = crc_function(binary, 0)
        if crc_bootloader != crc_loader:
            print('Error: CRC check failed. Expected: 0x{:04x}, Got: 0x{:04x}')
            return False
        print('CRC check passed. Binaries successfully loaded.')
        self.exit_bootloader_mode()
        return True

    def run_terminal(self):
        miniterm = serial.tools.miniterm.Miniterm(self.sp, echo=False, eol='crlf', filters=[
         'default'])
        miniterm.exit_character = serial.tools.miniterm.unichr(3)
        miniterm.set_rx_encoding('UTF-8')
        miniterm.set_tx_encoding('UTF-8')
        miniterm.start()
        try:
            miniterm.join(True)
        except KeyboardInterrupt:
            pass

        miniterm.join()
        miniterm.close()


def command_flash(args):
    binary = bytes([])
    for binary_filename in args.binary:
        try:
            with open(binary_filename, 'rb') as (f):
                binary += f.read()
        except Exception as e:
            print('Error opening and reading "{}"'.format(binary_filename))
            sys.exit(1)

    binary += bytes([0] * 8)
    tock_loader = TockLoader()
    success = tock_loader.open(port=args.port)
    if not success:
        print('Could not open the serial port. Make sure the board is plugged in.')
        sys.exit(1)
    success = tock_loader.flash_binary(binary, args.address)
    if not success:
        print('Could not flash the binaries.')
        sys.exit(1)


def command_listen(args):
    tock_loader = TockLoader()
    success = tock_loader.open(port=args.port)
    if not success:
        print('Could not open the serial port. Make sure the board is plugged in.')
        sys.exit(1)
    tock_loader.run_terminal()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', '-p', help='The serial port to use')
    subparser = parser.add_subparsers(title='Commands')
    flash = subparser.add_parser('flash', help='Flash binaries to the chip')
    flash.set_defaults(func=command_flash)
    flash.add_argument('binary', help='The binary file or files to flash to the chip', nargs='+')
    flash.add_argument('--address', '-a', help='Address to flash the binary at', type=lambda x: int(x, 0), default=196608)
    listen = subparser.add_parser('listen', help='Open a terminal to receive UART data')
    listen.set_defaults(func=command_listen)
    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        print('Missing Command. Run with --help to see supported commands.')
        sys.exit(1)


if __name__ == '__main__':
    main()