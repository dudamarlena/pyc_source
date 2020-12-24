# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\PyTrinamic\ic\TMC5072\TMC5072_register.py
# Compiled at: 2020-02-07 09:07:02
# Size of source mod 2**32: 3878 bytes
"""
Created on 20.09.2019

@author: JM
"""

class TMC5072_register:
    __doc__ = '\n    Define all registers of the TMC5072.\n\n    Each register is defined either as an integer or as a tuple of integers.\n    Each integer represents a register address. Tuples of addresses are used to\n    represent a register that exists multiple times for multiple motors.\n    '
    GCONF = 0
    GSTAT = 1
    IFCNT = 2
    SLAVECONF = 3
    INPUT___OUTPUT = 4
    INPUT = 4
    OUTPUT = 4
    X_COMPARE = 5
    PWMCONF = (16, 24)
    PWM_STATUS = (17, 25)
    RAMPMODE = (32, 64)
    XACTUAL = (33, 65)
    VACTUAL = (34, 66)
    VSTART = (35, 67)
    A1 = (36, 68)
    V1 = (37, 69)
    AMAX = (38, 70)
    VMAX = (39, 71)
    DMAX = (40, 72)
    D1 = (42, 74)
    VSTOP = (43, 75)
    TZEROWAIT = (44, 76)
    XTARGET = (45, 77)
    IHOLD_IRUN = (48, 80)
    VCOOLTHRS = (49, 81)
    VHIGH = (50, 82)
    VDCMIN = (51, 83)
    SWMODE = (52, 84)
    RAMPSTAT = (53, 85)
    XLATCH = (54, 86)
    ENCMODE = (56, 88)
    X_ENC = (57, 89)
    ENC_CONST = (58, 90)
    ENC_STATUS = (59, 91)
    ENC_LATCH = (60, 92)
    MSLUT__ = 96
    MSLUTSEL = 104
    MSLUTSTART = 105
    MSCNT = (106, 122)
    MSCURACT = (107, 123)
    CHOPCONF = (108, 124)
    COOLCONF = (109, 125)
    DCCTRL = (110, 126)
    DRVSTATUS = (111, 127)