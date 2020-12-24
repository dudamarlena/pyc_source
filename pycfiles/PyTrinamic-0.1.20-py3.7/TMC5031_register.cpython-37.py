# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\PyTrinamic\ic\TMC5031\TMC5031_register.py
# Compiled at: 2020-01-29 10:05:28
# Size of source mod 2**32: 2117 bytes
"""
Created on 29.01.2020

@author: JM
"""

class TMC5031_register:
    __doc__ = '\n    Define all registers of the TMC5031.\n\n    Each register is defined either as an integer or as a tuple of integers.\n    Each integer represents a register address. Tuples of addresses are used to\n    represent a register that exists multiple times for multiple motors.\n    '
    GCONF = 0
    GSTAT = 1
    SLAVECONF = 3
    INPUT = 4
    X_COMPARE = 5
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
    RAMPMODE_M2 = 64
    XACTUAL_M2 = 65
    VACTUAL_M2 = 66
    VSTART_M2 = 67
    A1_M2 = 68
    V1_M2 = 69
    AMAX_M2 = 70
    VMAX_M2 = 71
    DMAX_M2 = 72
    D1_M2 = 74
    VSTOP_M2 = 75
    TZEROWAIT_M2 = 76
    XTARGET_M2 = 77
    IHOLD_IRUN_M1 = 48
    VCOOLTHRS_M1 = 49
    VHIGH_M1 = 50
    SW_MODE_M1 = 52
    RAMP_STAT_M1 = 53
    XLATCH_M1 = 54
    IHOLD_IRUN_M2 = 80
    VCOOLTHRS_M2 = 81
    VHIGH_M2 = 82
    SW_MODE_M2 = 84
    RAMP_STAT_M2 = 85
    XLATCH_M2 = 86
    MSLUT___M1 = 96
    MSLUTSEL_M1 = 104
    MSLUTSTART_M1 = 105
    MSCNT_M1 = 106
    MSCURACT_M1 = 107
    CHOPCONF_M1 = 108
    COOLCONF_M1 = 109
    DRV_STATUS_M1 = 111
    MSLUT___M2 = 112
    MSLUTSEL_M2 = 120
    MSLUTSTART_M2 = 121
    MSCNT_M2 = 122
    MSCURACT_M2 = 123
    CHOPCONF_M2 = 124
    COOLCONF_M2 = 125
    DRV_STATUS_M2 = 127