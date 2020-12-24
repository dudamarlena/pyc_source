# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hexdutils/intohex.py
# Compiled at: 2019-08-02 01:46:08
# Size of source mod 2**32: 1125 bytes
from os import path
import sys
sys.path.insert(0, path.abspath(path.join(path.dirname(__file__), '.')))
from __hex_constants__ import __hex_letters, __alphabet

def _intohex(number, hex_prefix=False, uppercase=False):
    if type(number) is not int:
        raise TypeError('Value to convert must be int (is %s)' % type(number))
    isneg = None
    if number < 0:
        number = -number
        isneg = True

    def hexdivide(target):
        if target % 16 > 9:
            for item in __hex_letters:
                if __hex_letters[item] == target % 16:
                    if uppercase:
                        return item.upper()
                    return item

            return target % 16
        return target % 16

    values = []
    while number // 16 is not 0:
        values.insert(0, hexdivide(number))
        number = number // 16

    values.insert(0, hexdivide(number))
    if hex_prefix:
        return ('-' if isneg else '') + '0x' + ''.join((str(item) for item in values))
    return ('-' if isneg else '') + ''.join((str(item) for item in values))