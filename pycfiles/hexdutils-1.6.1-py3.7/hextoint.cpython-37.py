# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hexdutils/hextoint.py
# Compiled at: 2019-08-02 02:27:16
# Size of source mod 2**32: 1104 bytes
from os import path
import sys
sys.path.insert(0, path.abspath(path.join(path.dirname(__file__), '.')))
from __hex_constants__ import __hex_letters, __alphabet

def _hextoint(target):
    if type(target) is not str:
        raise TypeError('Argument must be str (is %s)' % type(target))
    else:
        decimals = []
        isneg_mult = None
        if target[0] == '-':
            isneg_mult = -1
            target = target[1:]
        else:
            isneg_mult = 1
    if target[:2] is '0x':
        target = target[2:]
    power_of_sixteen = len(target) - 1
    for item in target:
        try:
            decimals.append(int(item) * 16 ** power_of_sixteen)
            power_of_sixteen -= 1
        except:
            if item.lower() in __hex_letters:
                decimals.append(__hex_letters[item.lower()] * 16 ** power_of_sixteen)
            else:
                raise ValueError(item, "doesn't belong to hex system")

    else:
        return sum(decimals) * isneg_mult