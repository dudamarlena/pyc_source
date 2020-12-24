# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\PyTrinamic\ic\TMC5130\TMC5130_register.py
# Compiled at: 2019-12-05 10:30:00
# Size of source mod 2**32: 1641 bytes
"""
Created on 09.01.2019

@author: LK
"""

class TMC5130_register:
    __doc__ = '\n    Define all registers of the TMC5130.\n\n    Each register is defined either as an integer or as a tuple of integers.\n    Each integer represents a register address. Tuples of addresses are used to\n    represent a register that exists multiple times for multiple motors.\n    '
    GCONF = 0
    GSTAT = 1
    IFCNT = 2
    SLAVECONF = 3
    IOIN___OUTPUT = 4
    X_COMPARE = 5
    IHOLD_IRUN = 16
    TPOWERDOWN = 17
    TSTEP = 18
    TPWMTHRS = 19
    TCOOLTHRS = 20
    THIGH = 21
    RAMPMODE = 32
    XACTUAL = 33
    VACTUAL = 34
    VSTART = 35
    A1 = 36
    V1 = 37
    AMAX = 38
    VMAX = 39
    DMAX = 40
    D1 = 42
    VSTOP = 43
    TZEROWAIT = 44
    XTARGET = 45
    VDCMIN = 51
    SW_MODE = 52
    RAMP_STAT = 53
    XLATCH = 54
    ENCMODE = 56
    X_ENC = 57
    ENC_CONST = 58
    ENC_STATUS = 59
    ENC_LATCH = 60
    MSLUT__ = 96
    MSLUTSEL = 104
    MSLUTSTART = 105
    MSCNT = 106
    MSCURACT = 107
    CHOPCONF = 108
    COOLCONF = 109
    DCCTRL = 110
    DRV_STATUS = 111
    PWMCONF = 112
    PWM_SCALE = 113
    ENCM_CTRL = 114
    LOST_STEPS = 115