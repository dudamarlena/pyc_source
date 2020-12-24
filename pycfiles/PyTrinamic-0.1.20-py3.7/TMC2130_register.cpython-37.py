# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\PyTrinamic\ic\TMC2130\TMC2130_register.py
# Compiled at: 2019-12-05 10:24:30
# Size of source mod 2**32: 711 bytes
"""
Created on 14.10.2019

@author: JM
"""

class TMC2130_register:
    __doc__ = '\n    Define all registers of the TMC2130.\n    '
    GCONF = 0
    GSTAT = 1
    IOIN = 4
    IHOLD_IRUN = 16
    TPOWERDOWN = 17
    TSTEP = 18
    TPWMTHRS = 19
    TCOOLTHRS = 20
    THIGH = 21
    XDIRECT = 45
    VDCMIN = 51
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