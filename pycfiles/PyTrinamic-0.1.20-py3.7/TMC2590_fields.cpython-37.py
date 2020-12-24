# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\PyTrinamic\ic\TMC2590\TMC2590_fields.py
# Compiled at: 2020-02-07 08:53:41
# Size of source mod 2**32: 3411 bytes
"""
Created on 07.02.2020

@author: JM
"""

class TMC2590_fields(object):
    __doc__ = '\n\tDefine all register bitfields of the TMC2590.\n\n\tEach field is defined as a tuple consisting of ( Address, Mask, Shift ).\n\n\tThe name of the register is written as a comment behind each tuple. This is\n\tintended for IDE users viewing the definition of a field by hovering over\n\tit. This allows the user to see the corresponding register name of a field\n\twithout opening this file and searching for the definition.\n\t'
    MSTEP = (0, 1047552, 10)
    STST = (0, 128, 7)
    OLB = (0, 64, 6)
    OLA = (0, 32, 5)
    S2GB = (0, 16, 4)
    S2GA = (0, 8, 3)
    OTPW = (0, 4, 2)
    OT = (0, 2, 1)
    SG = (0, 1, 0)
    SE = (2, 31744, 10)
    REGISTER_ADDRESS_BITS = (8, 12582912, 18)
    INTPOL = (8, 512, 9)
    DEDGE = (8, 256, 8)
    MRES = (8, 15, 0)
    PHA = (8, 131072, 17)
    CA = (8, 130560, 9)
    PHB = (8, 256, 8)
    CB = (8, 255, 0)
    TBL = (12, 98304, 15)
    CHM = (12, 16384, 14)
    RNDTF = (12, 8192, 13)
    HDEC = (12, 6144, 11)
    HEND = (12, 1920, 7)
    HSTRT = (12, 112, 4)
    HDEC1 = (12, 8192, 12)
    HDEC0 = (12, 4096, 11)
    TOFF = (12, 15, 0)
    SEIMIN = (13, 32768, 15)
    SEDN = (13, 24576, 13)
    SEUP = (13, 96, 5)
    SEMAX = (13, 3840, 8)
    SEMIN = (13, 15, 0)
    SFILT = (14, 65536, 16)
    SGT = (14, 32512, 8)
    CS = (14, 31, 0)
    TST = (15, 65536, 16)
    SLPH = (15, 49152, 14)
    SLPL = (15, 12288, 12)
    DISS2G = (15, 1024, 10)
    TS2G = (15, 768, 8)
    SDOFF = (15, 128, 7)
    VSENSE = (15, 64, 6)
    RDSEL = (15, 48, 4)