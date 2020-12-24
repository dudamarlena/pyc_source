# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\PyTrinamic\ic\TMC5161\TMC5161_register.py
# Compiled at: 2020-01-30 03:09:51
# Size of source mod 2**32: 1622 bytes
"""
Created on 30.01.2020

@author: JM
"""

class TMC5161_register:
    __doc__ = '\n    Define all registers of the TMC5161.\n    '
    GCONF = 0
    GSTAT = 1
    IFCNT = 2
    SLAVECONF = 3
    IOIN___OUTPUT = 4
    X_COMPARE = 5
    OTP_PROG = 6
    OTP_READ = 7
    FACTORY_CONF = 8
    SHORT_CONF = 9
    DRV_CONF = 10
    GLOBAL_SCALER = 11
    OFFSET_READ = 12
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
    ENC_DEVIATION = 61
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
    PWM_AUTO = 114
    LOST_STEPS = 115