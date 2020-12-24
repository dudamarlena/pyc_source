# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\PyTrinamic\ic\TMC5041\TMC5041_register.py
# Compiled at: 2019-12-05 10:28:14
# Size of source mod 2**32: 2125 bytes
"""
Created on 18.04.2019

@author: LH
"""

class TMC5041_register:
    __doc__ = '\n    Define all registers of the TMC5041.\n\n    Each register is defined either as an integer or as a tuple of integers.\n    Each integer represents a register address. Tuples of addresses are used to\n    represent a register that exists multiple times for multiple motors.\n    '
    GCONF = 0
    GSTAT = 1
    IFCNT = 2
    TEST_SEL = 3
    INPUT = 4
    X_COMPARE = 5
    PWMCONF_M1 = 16
    PWM_STATUS_M1 = 17
    PWMCONF_M2 = 24
    PWM_STATUS_M2 = 25
    RAMPMODE_M1 = 32
    XACTUAL_M1 = 33
    VACTUAL_M1 = 34
    VSTART_M1 = 35
    A1_M1 = 36
    V1_M1 = 37
    AMAX_M1 = 38
    VMAX_M1 = 39
    DMAX_M1 = 40
    D1_M1 = 42
    VSTOP_M1 = 43
    TZEROWAIT_M1 = 44
    XTARGET_M1 = 45
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
    VDCMIN_M1 = 51
    SW_MODE_M1 = 52
    RAMP_STAT_M1 = 53
    XLATCH_M1 = 54
    IHOLD_IRUN_M2 = 80
    VCOOLTHRS_M2 = 81
    VHIGH_M2 = 82
    VDCMIN_M2 = 83
    SW_MODE_M2 = 84
    RAMP_STAT_M2 = 85
    XLATCH_M2 = 86
    MSLUT__ = 96
    MSLUTSEL = 104
    MSLUTSTART = 105
    MSCNT_M1 = 106
    MSCURACT_M1 = 107
    CHOPCONF_M1 = 108
    COOLCONF_M1 = 109
    DCCTRL_M1 = 110
    DRV_STATUS_M1 = 111
    MSCNT_M2 = 122
    MSCURACT_M2 = 123
    CHOPCONF_M2 = 124
    COOLCONF_M2 = 125
    DCCTRL_M2 = 126
    DRV_STATUS_M2 = 127