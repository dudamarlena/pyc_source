# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\crccheck\crc.py
# Compiled at: 2016-04-03 04:06:46
__doc__ = ' Classes to calculate CRCs (Cyclic Redundancy Check).\n\n  License::\n\n    Copyright (C) 2015-2016 by Martin Scharrer <martin@scharrer-online.de>\n\n    This program is free software: you can redistribute it and/or modify\n    it under the terms of the GNU General Public License as published by\n    the Free Software Foundation, either version 3 of the License, or\n    (at your option) any later version.\n\n    This program is distributed in the hope that it will be useful,\n    but WITHOUT ANY WARRANTY; without even the implied warranty of\n    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n    GNU General Public License for more details.\n\n    You should have received a copy of the GNU General Public License\n    along with this program.  If not, see <http://www.gnu.org/licenses/>.\n\n'
from crccheck.base import CrccheckBase, reflectbitorder, REFLECT_BIT_ORDER_TABLE

class CrcBase(CrccheckBase):
    """Abstract base class for all Cyclic Redundancy Checks (CRC) checksums"""
    _width = 0
    _poly = 0
    _initvalue = 0
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0
    _check_result = None
    _check_data = bytearray('123456789')

    def process(self, data):
        """ Process given data.

            Args:
                data (bytes, bytearray or list of ints [0-255]): input data to process.

            Returns:
                self
        """
        crc = self._value
        highbit = 1 << self._width - 1
        mask = highbit - 1 << 1 | 1
        poly = self._poly
        shift = self._width - 8
        diff8 = -shift
        if diff8 > 0:
            mask = 255
            crc <<= diff8
            shift = 0
            highbit = 128
            poly = self._poly << diff8
        reflect = self._reflect_input
        for byte in data:
            if reflect:
                byte = REFLECT_BIT_ORDER_TABLE[byte]
            crc ^= byte << shift
            for i in range(0, 8):
                if crc & highbit:
                    crc = crc << 1 ^ poly
                else:
                    crc = crc << 1

            crc &= mask

        if diff8 > 0:
            crc >>= diff8
        self._value = crc
        return self

    def final(self):
        """ Return final CRC value.

            Return:
                int: final CRC value
        """
        crc = self._value
        if self._reflect_output:
            crc = reflectbitorder(self._width, crc)
        crc ^= self._xor_output
        return crc


class Crc(CrcBase):
    """ Creates a new general (user-defined) CRC calculator instance.

        Arguments:
            width (int): bit width of CRC.
            poly (int): polynomial of CRC with the top bit omitted.
            initvalue (int): initial value of internal running CRC value. Usually either 0 or (1<<width)-1,
                i.e. "all-1s".
            reflect_input (bool): If true the bit order of the input bytes are reflected first.
                This is to calculate the CRC like least-significant bit first systems will do it.
            reflect_output (bool): If true the bit order of the calculation result will be reflected before
                the XOR output stage.
            xor_output (int): The result is bit-wise XOR-ed with this value. Usually 0 (value stays the same) or
                (1<<width)-1, i.e. "all-1s" (invert value).
            check_result (int): The expected result for the check input "123456789" (= [0x31, 0x32, 0x33, 0x34,
                0x35, 0x36, 0x37, 0x38, 0x39]). This value is used for the selftest() method to verify proper
                operation.
    """
    _width = 0
    _poly = 0
    _initvalue = 0
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0
    _check_result = None

    def __init__(self, width, poly, initvalue=0, reflect_input=False, reflect_output=False, xor_output=0, check_result=0):
        super(Crc, self).__init__(initvalue)
        self._width = width
        self._poly = poly
        self._reflect_input = reflect_input
        self._reflect_output = reflect_output
        self._xor_output = xor_output
        self._check_result = check_result


class Crc8(CrcBase):
    """CRC-8.
       Has optimised code for 8-bit CRCs and is used as base class for all other CRC with this width.
    """
    _width = 8
    _poly = 7
    _initvalue = 0
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0
    _check_result = 244

    def process(self, data):
        """ Process given data.

            Args:
                data (bytes, bytearray or list of ints [0-255]): input data to process.

            Returns:
                self
        """
        crc = self._value
        reflect = self._reflect_input
        poly = self._poly
        for byte in data:
            if reflect:
                byte = REFLECT_BIT_ORDER_TABLE[byte]
            crc = crc ^ byte
            for i in range(0, 8):
                if crc & 128:
                    crc = crc << 1 ^ poly
                else:
                    crc = crc << 1

            crc &= 255

        self._value = crc
        return self


class Crc16(CrcBase):
    """CRC-16.
       Has optimised code for 16-bit CRCs and is used as base class for all other CRC with this width.
    """
    _width = 16
    _poly = 4129
    _initvalue = 0
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0
    _check_result = 12739

    def process(self, data):
        """ Process given data.

            Args:
                data (bytes, bytearray or list of ints [0-255]): input data to process.

            Returns:
                self
        """
        crc = self._value
        reflect = self._reflect_input
        poly = self._poly
        for byte in data:
            if reflect:
                byte = REFLECT_BIT_ORDER_TABLE[byte]
            crc ^= byte << 8
            for i in range(0, 8):
                if crc & 32768:
                    crc = crc << 1 ^ poly
                else:
                    crc = crc << 1

            crc &= 65535

        self._value = crc
        return self


class Crc32(CrcBase):
    """CRC-32.
       Has optimised code for 32-bit CRCs and is used as base class for all other CRC with this width.
    """
    _width = 32
    _poly = 79764919
    _initvalue = 4294967295
    _reflect_input = True
    _reflect_output = True
    _xor_output = 4294967295
    _check_result = 3421780262

    def process(self, data):
        """ Process given data.

            Args:
                data (bytes, bytearray or list of ints [0-255]): input data to process.

            Returns:
                self
        """
        crc = self._value
        reflect = self._reflect_input
        poly = self._poly
        for byte in data:
            if reflect:
                byte = REFLECT_BIT_ORDER_TABLE[byte]
            crc ^= byte << 24
            for i in range(0, 8):
                if crc & 2147483648:
                    crc = crc << 1 ^ poly
                else:
                    crc = crc << 1

            crc &= 4294967295

        self._value = crc
        return self


class Crc3Rohc(CrcBase):
    """CRC-3/ROHC"""
    _width = 3
    _poly = 3
    _initvalue = 7
    _reflect_input = True
    _reflect_output = True
    _xor_output = 0
    _check_result = 6


class Crc4Itu(CrcBase):
    """CRC-4/ITU"""
    _width = 4
    _poly = 3
    _initvalue = 0
    _reflect_input = True
    _reflect_output = True
    _xor_output = 0
    _check_result = 7


class Crc5Epc(CrcBase):
    """CRC-5/EPC"""
    _width = 5
    _poly = 9
    _initvalue = 9
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0
    _check_result = 0


class Crc5Itu(CrcBase):
    """CRC-5/ITU"""
    _width = 5
    _poly = 21
    _initvalue = 0
    _reflect_input = True
    _reflect_output = True
    _xor_output = 0
    _check_result = 7


class Crc5Usb(CrcBase):
    """CRC-5/USB"""
    _width = 5
    _poly = 5
    _initvalue = 31
    _reflect_input = True
    _reflect_output = True
    _xor_output = 31
    _check_result = 25


class Crc6Cdma2000A(CrcBase):
    """CRC-6/CDMA2000-A"""
    _width = 6
    _poly = 39
    _initvalue = 63
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0
    _check_result = 13


class Crc6Cdma2000B(CrcBase):
    """CRC-6/CDMA2000-B"""
    _width = 6
    _poly = 7
    _initvalue = 63
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0
    _check_result = 59


class Crc6Darc(CrcBase):
    """CRC-6/DARC"""
    _width = 6
    _poly = 25
    _initvalue = 0
    _reflect_input = True
    _reflect_output = True
    _xor_output = 0
    _check_result = 38


class Crc6Itu(CrcBase):
    """CRC-6/ITU"""
    _width = 6
    _poly = 3
    _initvalue = 0
    _reflect_input = True
    _reflect_output = True
    _xor_output = 0
    _check_result = 6


class Crc7(CrcBase):
    """CRC-7"""
    _width = 7
    _poly = 9
    _initvalue = 0
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0
    _check_result = 117


class Crc7Rohc(CrcBase):
    """CRC-7/ROHC"""
    _width = 7
    _poly = 79
    _initvalue = 127
    _reflect_input = True
    _reflect_output = True
    _xor_output = 0
    _check_result = 83


class Crc8Cdma2000(Crc8):
    """CRC-8/CDMA2000"""
    _width = 8
    _poly = 155
    _initvalue = 255
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0
    _check_result = 218


class Crc8Darc(Crc8):
    """CRC-8/DARC"""
    _width = 8
    _poly = 57
    _initvalue = 0
    _reflect_input = True
    _reflect_output = True
    _xor_output = 0
    _check_result = 21


class Crc8DvbS2(Crc8):
    """CRC-8/DVB-S2"""
    _width = 8
    _poly = 213
    _initvalue = 0
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0
    _check_result = 188


class Crc8Ebu(Crc8):
    """CRC-8/EBU"""
    _width = 8
    _poly = 29
    _initvalue = 255
    _reflect_input = True
    _reflect_output = True
    _xor_output = 0
    _check_result = 151


class Crc8ICode(Crc8):
    """CRC-8/I-CODE"""
    _width = 8
    _poly = 29
    _initvalue = 253
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0
    _check_result = 126


class Crc8Itu(Crc8):
    """CRC-8/ITU"""
    _width = 8
    _poly = 7
    _initvalue = 0
    _reflect_input = False
    _reflect_output = False
    _xor_output = 85
    _check_result = 161


class Crc8Maxim(Crc8):
    """CRC-8/MAXIM"""
    _width = 8
    _poly = 49
    _initvalue = 0
    _reflect_input = True
    _reflect_output = True
    _xor_output = 0
    _check_result = 161


class Crc8Rohc(Crc8):
    """CRC-8/ROHC"""
    _width = 8
    _poly = 7
    _initvalue = 255
    _reflect_input = True
    _reflect_output = True
    _xor_output = 0
    _check_result = 208


class Crc8Wcdma(Crc8):
    """CRC-8/WCDMA"""
    _width = 8
    _poly = 155
    _initvalue = 0
    _reflect_input = True
    _reflect_output = True
    _xor_output = 0
    _check_result = 37


class Crc10(CrcBase):
    """CRC-10"""
    _width = 10
    _poly = 563
    _initvalue = 0
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0
    _check_result = 409


class Crc10Cdma2000(CrcBase):
    """CRC-10/CDMA2000"""
    _width = 10
    _poly = 985
    _initvalue = 1023
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0
    _check_result = 563


class Crc11(CrcBase):
    """CRC-11"""
    _width = 11
    _poly = 901
    _initvalue = 26
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0
    _check_result = 1443


class Crc123Gpp(CrcBase):
    """CRC-12/3GPP"""
    _width = 12
    _poly = 2063
    _initvalue = 0
    _reflect_input = False
    _reflect_output = True
    _xor_output = 0
    _check_result = 3503


class Crc12Cdma2000(CrcBase):
    """CRC-12/CDMA2000"""
    _width = 12
    _poly = 3859
    _initvalue = 4095
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0
    _check_result = 3405


class Crc12Dect(CrcBase):
    """CRC-12/DECT"""
    _width = 12
    _poly = 2063
    _initvalue = 0
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0
    _check_result = 3931


class Crc13Bbc(CrcBase):
    """CRC-13/BBC"""
    _width = 13
    _poly = 7413
    _initvalue = 0
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0
    _check_result = 1274


class Crc14Darc(CrcBase):
    """CRC-14/DARC"""
    _width = 14
    _poly = 2053
    _initvalue = 0
    _reflect_input = True
    _reflect_output = True
    _xor_output = 0
    _check_result = 2093


class Crc15(CrcBase):
    """CRC-15"""
    _width = 15
    _poly = 17817
    _initvalue = 0
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0
    _check_result = 1438


class Crc15Mpt1327(CrcBase):
    """CRC-15/MPT1327"""
    _width = 15
    _poly = 26645
    _initvalue = 0
    _reflect_input = False
    _reflect_output = False
    _xor_output = 1
    _check_result = 9574


class CrcArc(Crc16):
    """ARC"""
    _width = 16
    _poly = 32773
    _initvalue = 0
    _reflect_input = True
    _reflect_output = True
    _xor_output = 0
    _check_result = 47933


class Crc16AugCcitt(Crc16):
    """CRC-16/AUG-CCITT"""
    _width = 16
    _poly = 4129
    _initvalue = 7439
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0
    _check_result = 58828


class Crc16Buypass(Crc16):
    """CRC-16/BUYPASS"""
    _width = 16
    _poly = 32773
    _initvalue = 0
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0
    _check_result = 65256


class Crc16CcittFalse(Crc16):
    """CRC-16/CCITT-FALSE"""
    _width = 16
    _poly = 4129
    _initvalue = 65535
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0
    _check_result = 10673


class Crc16Cdma2000(Crc16):
    """CRC-16/CDMA2000"""
    _width = 16
    _poly = 51303
    _initvalue = 65535
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0
    _check_result = 19462


class Crc16Dds110(Crc16):
    """CRC-16/DDS-110"""
    _width = 16
    _poly = 32773
    _initvalue = 32781
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0
    _check_result = 40655


class Crc16DectR(Crc16):
    """CRC-16/DECT-R"""
    _width = 16
    _poly = 1417
    _initvalue = 0
    _reflect_input = False
    _reflect_output = False
    _xor_output = 1
    _check_result = 126


class Crc16DectX(Crc16):
    """CRC-16/DECT-X"""
    _width = 16
    _poly = 1417
    _initvalue = 0
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0
    _check_result = 127


class Crc16Dnp(Crc16):
    """CRC-16/DNP"""
    _width = 16
    _poly = 15717
    _initvalue = 0
    _reflect_input = True
    _reflect_output = True
    _xor_output = 65535
    _check_result = 60034


class Crc16En13757(Crc16):
    """CRC-16/EN-13757"""
    _width = 16
    _poly = 15717
    _initvalue = 0
    _reflect_input = False
    _reflect_output = False
    _xor_output = 65535
    _check_result = 49847


class Crc16Genibus(Crc16):
    """CRC-16/GENIBUS"""
    _width = 16
    _poly = 4129
    _initvalue = 65535
    _reflect_input = False
    _reflect_output = False
    _xor_output = 65535
    _check_result = 54862


class Crc16Maxim(Crc16):
    """CRC-16/MAXIM"""
    _width = 16
    _poly = 32773
    _initvalue = 0
    _reflect_input = True
    _reflect_output = True
    _xor_output = 65535
    _check_result = 17602


class Crcc16Mcrf4xx(Crc16):
    """CRC-16/MCRF4XX"""
    _width = 16
    _poly = 4129
    _initvalue = 65535
    _reflect_input = True
    _reflect_output = True
    _xor_output = 0
    _check_result = 28561


class Crc16Riello(Crc16):
    """CRC-16/RIELLO"""
    _width = 16
    _poly = 4129
    _initvalue = 45738
    _reflect_input = True
    _reflect_output = True
    _xor_output = 0
    _check_result = 25552


class Crc16T10Dif(Crc16):
    """CRC-16/T10-DIF"""
    _width = 16
    _poly = 35767
    _initvalue = 0
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0
    _check_result = 53467


class Crc16Teledisk(Crc16):
    """CRC-16/TELEDISK"""
    _width = 16
    _poly = 41111
    _initvalue = 0
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0
    _check_result = 4019


class Crc16Tms37157(Crc16):
    """CRC-16/TMS37157"""
    _width = 16
    _poly = 4129
    _initvalue = 35308
    _reflect_input = True
    _reflect_output = True
    _xor_output = 0
    _check_result = 9905


class Crc16Usb(Crc16):
    """CRC-16/USB"""
    _width = 16
    _poly = 32773
    _initvalue = 65535
    _reflect_input = True
    _reflect_output = True
    _xor_output = 65535
    _check_result = 46280


class CrcA(Crc16):
    """CRC-A"""
    _width = 16
    _poly = 4129
    _initvalue = 50886
    _reflect_input = True
    _reflect_output = True
    _xor_output = 0
    _check_result = 48901


class Crc16Ccitt(Crc16):
    """CRC16 CCITT, aka KERMIT"""
    _width = 16
    _poly = 4129
    _initvalue = 0
    _reflect_input = True
    _reflect_output = True
    _xor_output = 0
    _check_result = 8585


CrcKermit = Crc16Ccitt

class CrcModbus(CrcBase):
    """MODBUS"""
    _width = 16
    _poly = 32773
    _initvalue = 65535
    _reflect_input = True
    _reflect_output = True
    _xor_output = 0
    _check_result = 19255


class CrcX25(CrcBase):
    """X-25"""
    _width = 16
    _poly = 4129
    _initvalue = 65535
    _reflect_input = True
    _reflect_output = True
    _xor_output = 65535
    _check_result = 36974


class CrcXmodem(CrcBase):
    """XMODEM"""
    _width = 16
    _poly = 4129
    _initvalue = 0
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0
    _check_result = 12739


class Crc24(CrcBase):
    """CRC-24"""
    _width = 24
    _poly = 8801531
    _initvalue = 11994318
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0
    _check_result = 2215682


class Crc24FlexrayA(CrcBase):
    """CRC-24/FLEXRAY-A"""
    _width = 24
    _poly = 6122955
    _initvalue = 16702650
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0
    _check_result = 7961021


class Crc24FlexrayB(CrcBase):
    """CRC-24/FLEXRAY-B"""
    _width = 24
    _poly = 6122955
    _initvalue = 11259375
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0
    _check_result = 2040760


class Crc31Philips(CrcBase):
    """CRC-31/PHILIPS"""
    _width = 31
    _poly = 79764919
    _initvalue = 2147483647
    _reflect_input = False
    _reflect_output = False
    _xor_output = 2147483647
    _check_result = 216654956


class Crc32Bzip2(Crc32):
    """CRC-32/BZIP2"""
    _width = 32
    _poly = 79764919
    _initvalue = 4294967295
    _reflect_input = False
    _reflect_output = False
    _xor_output = 4294967295
    _check_result = 4236843288


class Crc32c(Crc32):
    """CRC-32C"""
    _width = 32
    _poly = 517762881
    _initvalue = 4294967295
    _reflect_input = True
    _reflect_output = True
    _xor_output = 4294967295
    _check_result = 3808858755


class Crc32d(Crc32):
    """CRC-32D"""
    _width = 32
    _poly = 2821953579
    _initvalue = 4294967295
    _reflect_input = True
    _reflect_output = True
    _xor_output = 4294967295
    _check_result = 2268157302


class Crc32Mpeg2(Crc32):
    """CRC-32/MPEG-2"""
    _width = 32
    _poly = 79764919
    _initvalue = 4294967295
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0
    _check_result = 58124007


class Crc32Posix(Crc32):
    """CRC-32/POSIX"""
    _width = 32
    _poly = 79764919
    _initvalue = 0
    _reflect_input = False
    _reflect_output = False
    _xor_output = 4294967295
    _check_result = 1985902208


class Crc32q(Crc32):
    """CRC-32Q"""
    _width = 32
    _poly = 2168537515
    _initvalue = 0
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0
    _check_result = 806403967


class CrcJamcrc(Crc32):
    """JAMCRC"""
    _width = 32
    _poly = 79764919
    _initvalue = 4294967295
    _reflect_input = True
    _reflect_output = True
    _xor_output = 0
    _check_result = 873187033


class CrcXfer(Crc32):
    """XFER"""
    _width = 32
    _poly = 175
    _initvalue = 0
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0
    _check_result = 3171672888


class Crc40Gsm(CrcBase):
    """CRC-40/GSM"""
    _width = 40
    _poly = 75628553
    _initvalue = 0
    _reflect_input = False
    _reflect_output = False
    _xor_output = 1099511627775
    _check_result = 910907393606


class Crc64(CrcBase):
    """CRC-64"""
    _width = 64
    _poly = 4823603603198064275
    _initvalue = 0
    _reflect_input = False
    _reflect_output = False
    _xor_output = 0
    _check_result = 7800480153909949255


class Crc64We(CrcBase):
    """CRC-64/WE"""
    _width = 64
    _poly = 4823603603198064275
    _initvalue = 18446744073709551615
    _reflect_input = False
    _reflect_output = False
    _xor_output = 18446744073709551615
    _check_result = 7128171145767219210


class Crc64Xz(CrcBase):
    """CRC-64/XZ"""
    _width = 64
    _poly = 4823603603198064275
    _initvalue = 18446744073709551615
    _reflect_input = True
    _reflect_output = True
    _xor_output = 18446744073709551615
    _check_result = 11051210869376104954


class Crc82Darc(CrcBase):
    """CRC-82/DARC"""
    _width = 82
    _poly = 229256212191916381701137
    _initvalue = 0
    _reflect_input = True
    _reflect_output = True
    _xor_output = 0
    _check_result = 749237524598872659187218


ALLCRCCLASSES = (
 Crc3Rohc, Crc4Itu, Crc5Epc, Crc5Itu, Crc5Usb, Crc6Cdma2000A, Crc6Cdma2000B, Crc6Darc, Crc6Itu, Crc7, Crc7Rohc,
 Crc8, Crc8Cdma2000, Crc8Darc, Crc8DvbS2, Crc8Ebu, Crc8ICode, Crc8Itu, Crc8Maxim, Crc8Rohc, Crc8Wcdma, Crc10,
 Crc10Cdma2000, Crc11, Crc123Gpp, Crc12Cdma2000, Crc12Dect, Crc13Bbc, Crc14Darc, Crc15, Crc15Mpt1327, Crc16, CrcArc,
 Crc16AugCcitt, Crc16Buypass, Crc16CcittFalse, Crc16Cdma2000, Crc16Dds110, Crc16DectR, Crc16DectX, Crc16Dnp,
 Crc16En13757, Crc16Genibus, Crc16Maxim, Crcc16Mcrf4xx, Crc16Riello, Crc16T10Dif, Crc16Teledisk, Crc16Tms37157,
 Crc16Usb, CrcA, Crc16Ccitt, CrcKermit, CrcModbus, CrcX25, CrcXmodem, Crc24, Crc24FlexrayA, Crc24FlexrayB,
 Crc31Philips, Crc32, Crc32Bzip2, Crc32c, Crc32d, Crc32Mpeg2, Crc32Posix, Crc32q, CrcJamcrc, CrcXfer, Crc40Gsm,
 Crc64, Crc64We, Crc64Xz, Crc82Darc)