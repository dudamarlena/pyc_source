# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pifi/Adafruit_I2C.py
# Compiled at: 2014-10-22 23:54:57
import smbus

class Adafruit_I2C:

    @staticmethod
    def getPiRevision():
        """Gets the version number of the Raspberry Pi board"""
        try:
            with open('/proc/cpuinfo', 'r') as (f):
                for line in f:
                    if line.startswith('Revision'):
                        if line.rstrip()[(-1)] in ('1', '2'):
                            return 1
                        return 2

        except:
            return 0

    @staticmethod
    def getPiI2CBusNumber():
        if Adafruit_I2C.getPiRevision() > 1:
            return 1
        return 0

    def __init__(self, address, busnum=-1, debug=False):
        self.address = address
        self.bus = smbus.SMBus(busnum if busnum >= 0 else Adafruit_I2C.getPiI2CBusNumber())
        self.debug = debug

    def reverseByteOrder(self, data):
        """Reverses the byte order of an int (16-bit) or long (32-bit) value"""
        byteCount = len(hex(data)[2:].replace('L', '')[::2])
        val = 0
        for i in range(byteCount):
            val = val << 8 | data & 255
            data >>= 8

        return val

    def errMsg(self):
        print 'Error accessing 0x%02X: Check your I2C address' % self.address
        return -1

    def write8(self, reg, value):
        """Writes an 8-bit value to the specified register/address"""
        try:
            self.bus.write_byte_data(self.address, reg, value)
            if self.debug:
                print 'I2C: Wrote 0x%02X to register 0x%02X' % (value, reg)
        except IOError as err:
            return self.errMsg()

    def write16(self, reg, value):
        """Writes a 16-bit value to the specified register/address pair"""
        try:
            self.bus.write_word_data(self.address, reg, value)
            if self.debug:
                print 'I2C: Wrote 0x%02X to register pair 0x%02X,0x%02X' % (
                 value, reg, reg + 1)
        except IOError as err:
            return self.errMsg()

    def writeList(self, reg, list):
        """Writes an array of bytes using I2C format"""
        try:
            if self.debug:
                print 'I2C: Writing list to register 0x%02X:' % reg
                print list
            self.bus.write_i2c_block_data(self.address, reg, list)
        except IOError as err:
            return self.errMsg()

    def readList(self, reg, length):
        """Read a list of bytes from the I2C device"""
        try:
            results = self.bus.read_i2c_block_data(self.address, reg, length)
            if self.debug:
                print 'I2C: Device 0x%02X returned the following from reg 0x%02X' % (
                 self.address, reg)
                print results
            return results
        except IOError as err:
            return self.errMsg()

    def readU8(self, reg):
        """Read an unsigned byte from the I2C device"""
        try:
            result = self.bus.read_byte_data(self.address, reg)
            if self.debug:
                print 'I2C: Device 0x%02X returned 0x%02X from reg 0x%02X' % (
                 self.address, result & 255, reg)
            return result
        except IOError as err:
            return self.errMsg()

    def readS8(self, reg):
        """Reads a signed byte from the I2C device"""
        try:
            result = self.bus.read_byte_data(self.address, reg)
            if result > 127:
                result -= 256
            if self.debug:
                print 'I2C: Device 0x%02X returned 0x%02X from reg 0x%02X' % (
                 self.address, result & 255, reg)
            return result
        except IOError as err:
            return self.errMsg()

    def readU16(self, reg):
        """Reads an unsigned 16-bit value from the I2C device"""
        try:
            result = self.bus.read_word_data(self.address, reg)
            if self.debug:
                print 'I2C: Device 0x%02X returned 0x%04X from reg 0x%02X' % (self.address, result & 65535, reg)
            return result
        except IOError as err:
            return self.errMsg()

    def readS16(self, reg):
        """Reads a signed 16-bit value from the I2C device"""
        try:
            result = self.bus.read_word_data(self.address, reg)
            if self.debug:
                print 'I2C: Device 0x%02X returned 0x%04X from reg 0x%02X' % (self.address, result & 65535, reg)
            return result
        except IOError as err:
            return self.errMsg()


if __name__ == '__main__':
    try:
        bus = Adafruit_I2C(address=0)
        print 'Default I2C bus is accessible'
    except:
        print 'Error accessing default I2C bus'