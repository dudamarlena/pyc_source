# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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