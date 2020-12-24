# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/pyasn1/pyasn1/compat/binary.py
# Compiled at: 2018-07-11 18:15:32
from sys import version_info
if version_info[0:2] < (2, 6):

    def bin(value):
        bitstring = []
        if value > 0:
            prefix = '0b'
        else:
            if value < 0:
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