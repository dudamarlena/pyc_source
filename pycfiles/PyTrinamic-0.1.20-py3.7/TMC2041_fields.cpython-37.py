# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\PyTrinamic\ic\TMC2041\TMC2041_fields.py
# Compiled at: 2019-12-05 09:37:53
# Size of source mod 2**32: 8640 bytes
"""
Created on 24.10.2019

@author: JM
"""

class TMC2041_fields(object):
    __doc__ = '\n\tDefine all register bitfields of the TMC2041.\n\n\tEach field is defined as a tuple consisting of ( Address, Mask, Shift ).\n\n\tThe name of the register is written as a comment behind each tuple. This is\n\tintended for IDE users viewing the definition of a field by hovering over\n\tit. This allows the user to see the corresponding register name of a field\n\twithout opening this file and searching for the definition.\n\t'
    TEST_MODE = (0, 128, 7)
    SHAFT1 = (0, 256, 8)
    SHAFT2 = (0, 512, 9)
    LOCK_GCONF = (0, 1024, 10)
    RESET = (1, 1, 0)
    DRV_ERR1 = (1, 2, 1)
    DRV_ERR2 = (1, 4, 2)
    UV_CP = (1, 8, 3)
    IFCNT = (2, 255, 0)
    TEST_SEL = (3, 15, 0)
    DRV_ENN = (4, 128, 7)
    VERSION = (4, 4278190080, 24)
    IHOLD = (48, 31, 0)
    IRUN = (48, 7936, 8)
    IHOLDDELAY = (48, 983040, 16)
    IHOLD = (80, 31, 0)
    IRUN = (80, 7936, 8)
    IHOLDDELAY = (80, 983040, 16)
    MSCNT = (106, 1023, 0)
    CUR_A = (107, 511, 0)
    CUR_B = (107, 33488896, 16)
    TOFF = (108, 15, 0)
    TFD_2__0_ = (108, 112, 4)
    OFFSET = (108, 1920, 7)
    TFD__ = (108, 2048, 11)
    DISFDCC = (108, 4096, 12)
    RNDTF = (108, 8192, 13)
    CHM = (108, 16384, 14)
    TBL = (108, 98304, 15)
    VSENSE = (108, 131072, 17)
    VHIGHFS = (108, 262144, 18)
    VHIGHCHM = (108, 524288, 19)
    SYNC = (108, 15728640, 20)
    MRES = (108, 251658240, 24)
    INTPOL16 = (108, 268435456, 28)
    DEDGE = (108, 536870912, 29)
    DISS2G = (108, 1073741824, 30)
    TOFF = (108, 15, 0)
    TFD_2__0_ = (108, 112, 4)
    OFFSET = (108, 1920, 7)
    TFD__ = (108, 2048, 11)
    DISFDCC = (108, 4096, 12)
    RNDTF = (108, 8192, 13)
    CHM = (108, 16384, 14)
    TBL = (108, 98304, 15)
    VSENSE = (108, 131072, 17)
    VHIGHFS = (108, 262144, 18)
    VHIGHCHM = (108, 524288, 19)
    SYNC = (108, 15728640, 20)
    MRES = (108, 251658240, 24)
    INTPOL16 = (108, 268435456, 28)
    DEDGE = (108, 536870912, 29)
    DISS2G = (108, 1073741824, 30)
    TOFF = (108, 15, 0)
    HSTRT = (108, 112, 4)
    HEND = (108, 1920, 7)
    RNDTF = (108, 8192, 13)
    CHM = (108, 16384, 14)
    TBL = (108, 98304, 15)
    VSENSE = (108, 131072, 17)
    VHIGHFS = (108, 262144, 18)
    VHIGHCHM = (108, 524288, 19)
    SYNC = (108, 15728640, 20)
    MRES = (108, 251658240, 24)
    INTPOL16 = (108, 268435456, 28)
    DEDGE = (108, 536870912, 29)
    DISS2G = (108, 1073741824, 30)
    SEMIN = (109, 15, 0)
    SEUP = (109, 96, 5)
    SEMAX = (109, 3840, 8)
    SEDN = (109, 24576, 13)
    SEIMIN = (109, 32768, 15)
    SGT = (109, 8323072, 16)
    SFILT = (109, 16777216, 24)
    SG_RESULT = (111, 1023, 0)
    FSACTIVE = (111, 32768, 15)
    CS_ACTUAL = (111, 2031616, 16)
    STALLGUARD = (111, 16777216, 24)
    OT = (111, 33554432, 25)
    OTPW = (111, 67108864, 26)
    S2GA = (111, 134217728, 27)
    S2GB = (111, 268435456, 28)
    OLA = (111, 536870912, 29)
    OLB = (111, 1073741824, 30)
    STST = (111, 2147483648, 31)
    MSCNT = (122, 1023, 0)
    CUR_A = (123, 511, 0)
    CUR_B = (123, 33488896, 16)
    TOFF = (124, 15, 0)
    TFD_2__0_ = (124, 112, 4)
    OFFSET = (124, 1920, 7)
    TFD__ = (124, 2048, 11)
    DISFDCC = (124, 4096, 12)
    RNDTF = (124, 8192, 13)
    CHM = (124, 16384, 14)
    TBL = (124, 98304, 15)
    VSENSE = (124, 131072, 17)
    VHIGHFS = (124, 262144, 18)
    VHIGHCHM = (124, 524288, 19)
    SYNC = (124, 15728640, 20)
    DISS2G = (124, 1073741824, 30)
    TOFF = (124, 15, 0)
    TFD_2__0_ = (124, 112, 4)
    OFFSET = (124, 1920, 7)
    TFD__ = (124, 2048, 11)
    DISFDCC = (124, 4096, 12)
    RNDTF = (124, 8192, 13)
    CHM = (124, 16384, 14)
    TBL = (124, 98304, 15)
    VSENSE = (124, 131072, 17)
    VHIGHFS = (124, 262144, 18)
    VHIGHCHM = (124, 524288, 19)
    SYNC = (124, 15728640, 20)
    DISS2G = (124, 1073741824, 30)
    TOFF = (124, 15, 0)
    HSTRT = (124, 112, 4)
    HEND = (124, 1920, 7)
    RNDTF = (124, 8192, 13)
    CHM = (124, 16384, 14)
    TBL = (124, 98304, 15)
    VSENSE = (124, 131072, 17)
    VHIGHFS = (124, 262144, 18)
    VHIGHCHM = (124, 524288, 19)
    SYNC = (124, 15728640, 20)
    DISS2G = (124, 1073741824, 30)
    SEMIN = (125, 15, 0)
    SEUP = (125, 96, 5)
    SEMAX = (125, 3840, 8)
    SEDN = (125, 24576, 13)
    SEIMIN = (125, 32768, 15)
    SGT = (125, 8323072, 16)
    SFILT = (125, 16777216, 24)
    SG_RESULT = (127, 1023, 0)
    FSACTIVE = (127, 32768, 15)
    CS_ACTUAL = (127, 2031616, 16)
    STALLGUARD = (127, 16777216, 24)
    OT = (127, 33554432, 25)
    OTPW = (127, 67108864, 26)
    S2GA = (127, 134217728, 27)
    S2GB = (127, 268435456, 28)
    OLA = (127, 536870912, 29)
    OLB = (127, 1073741824, 30)
    STST = (127, 2147483648, 31)