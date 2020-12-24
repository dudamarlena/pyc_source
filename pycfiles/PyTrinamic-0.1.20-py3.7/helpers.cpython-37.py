# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\PyTrinamic\helpers.py
# Compiled at: 2020-02-03 03:37:44
# Size of source mod 2**32: 539 bytes
"""
Created on 09.01.2019

@author: LK
"""
from PyTrinamic import name, desc

class TMC_helpers(object):

    @staticmethod
    def field_get(data, mask, shift):
        return (data & mask) >> shift

    @staticmethod
    def field_set(data, mask, shift, value):
        return data & ~mask | value << shift & mask

    @staticmethod
    def toSigned32(x):
        m = x & 4294967295
        return (m ^ 2147483648) - 2147483648

    @staticmethod
    def showInfo():
        print(name + ' - ' + desc)