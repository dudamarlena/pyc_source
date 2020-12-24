# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1/compat/binary.py
# Compiled at: 2019-10-17 01:00:19
from sys import version_info
if version_info[0:2] < (2, 6):

    def bin(value):
        bitstring = []
        if value > 0:
            prefix = '0b'
        elif value < 0:
            prefix = '-0b'
            value = abs(value)
        else:
            prefix = '0b0'
        while value:
            if value & 1 == 1:
                bitstring.append('1')
            else:
                bitstring.append('0')
            value >>= 1

        bitstring.reverse()
        return prefix + ('').join(bitstring)


else:
    bin = bin