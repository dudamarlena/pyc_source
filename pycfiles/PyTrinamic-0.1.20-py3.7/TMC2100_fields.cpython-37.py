# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\PyTrinamic\ic\TMC2100\TMC2100_fields.py
# Compiled at: 2019-12-05 09:40:04
# Size of source mod 2**32: 565 bytes
"""
Created on 15.10.2019

@author: JM
"""

class TMC2100_fields(object):
    __doc__ = '\n\tDefine all register bitfields of the TMC2100.\n\n\tEach field is defined as a tuple consisting of ( Address, Mask, Shift ).\n\n\tThe name of the register is written as a comment behind each tuple. This is\n\tintended for IDE users viewing the definition of a field by hovering over\n\tit. This allows the user to see the corresponding register name of a field\n\twithout opening this file and searching for the definition.\n\t'
    GCONF = (0, 4294967295, 0)