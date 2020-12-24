# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\PyTrinamic\ic\TMC6200\TMC6200_fields.py
# Compiled at: 2019-12-05 09:51:59
# Size of source mod 2**32: 3126 bytes
"""
Created on 06.03.2019

@author: ed
"""

class TMC6200_fields(object):
    DISABLE = (0, 1, 0)
    SINGLELINE = (0, 2, 1)
    FAULTDIRECT = (0, 4, 2)
    UNUSED = (0, 8, 3)
    AMPLIFICATION = (0, 48, 4)
    AMPLIFIER_OFF = (0, 64, 6)
    TEST_MODE = (0, 128, 7)
    RESET = (1, 1, 0)
    DRV_OTPW = (1, 2, 1)
    DRV_OT = (1, 4, 2)
    UV_CP = (1, 8, 3)
    SHORTDET_U = (1, 16, 4)
    S2GU = (1, 32, 5)
    S2VSU = (1, 64, 6)
    SHORTDET_V = (1, 256, 8)
    S2GV = (1, 512, 9)
    S2VSV = (1, 1024, 10)
    SHORTDET_W = (1, 4096, 12)
    S2GW = (1, 8192, 13)
    S2VSW = (1, 16384, 14)
    UL = (4, 1, 0)
    UH = (4, 2, 1)
    VL = (4, 4, 2)
    VH = (4, 8, 3)
    WL = (4, 16, 4)
    WH = (4, 32, 5)
    DRV_EN = (4, 64, 6)
    OTPW = (4, 256, 8)
    OT136_C = (4, 512, 9)
    OT143_C = (4, 1024, 10)
    OT150_C = (4, 2048, 11)
    VERSION = (4, 4278190080, 24)
    OTPBIT = (6, 7, 0)
    OTPBYTE = (6, 48, 4)
    OTPMAGIC = (6, 65280, 8)
    OTP_BBM = (7, 192, 6)
    OTP_S2_LEVEL = (7, 32, 5)
    OTP_FCLKTRIM = (7, 31, 0)
    FACTORY_CONF = (8, 31, 0)
    S2VS_LEVEL = (9, 15, 0)
    S2G_LEVEL = (9, 3840, 8)
    SHORTFILTER = (9, 196608, 16)
    SHORTDELAY = (9, 1048576, 20)
    RETRY = (9, 50331648, 24)
    PROTECT_PARALLEL = (9, 268435456, 28)
    DISABLE_S2G = (9, 536870912, 29)
    DISABLE_S2VS = (9, 1073741824, 30)
    BBMCLKS = (10, 15, 0)
    OTSELECT = (10, 196608, 16)
    DRVSTRENGTH = (10, 786432, 18)