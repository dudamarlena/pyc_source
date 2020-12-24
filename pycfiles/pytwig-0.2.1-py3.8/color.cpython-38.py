# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pytwig/color.py
# Compiled at: 2019-12-01 22:29:38
# Size of source mod 2**32: 1214 bytes
import struct
from pytwig.src.lib import util

class Color:
    __doc__ = 'Data storage object that contains parameters for Bitwig colors.\n\t'

    def __init__(self, rd, gr, bl, al=1.0):
        """Initialization for Color object

                Reads color and alpha values and stores them in an array. If alpha value is 1.0, it is ignored and data array is length 3.

                Args:
                        rd (float): Red
                        gr (float): Green
                        bl (float): Blue
                        al (float): Alpha
                """
        self.type = 'color'
        self.data = [rd, gr, bl, al]
        if al == 1.0:
            self.data = self.data[:-1]

    def __iter__(self):
        yield (
         'type', self.type)
        yield ('data', self.data)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return 'Color: ' + str(self.data)

    def show(self):
        print(str(self.__dict__()).replace(', ', ',\n').replace('{', '{\n').replace('}', '\n}'))

    def encode(self):
        """Encodes the color object into Bitwig bytecode.

                Returns:
                        bytes: Bitwig bytecode representation of the Color object.
                """
        output = b''
        count = 0
        for item in self.data:
            flVal = struct.unpack('>I', struct.pack('>f', item))[0]
            output += util.hex_pad(flVal, 8)
            count += 1
        else:
            if count == 3:
                output += struct.pack('>f', 1.0)
            return output