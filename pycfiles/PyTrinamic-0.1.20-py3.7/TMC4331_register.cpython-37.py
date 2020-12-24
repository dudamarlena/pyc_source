# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\PyTrinamic\ic\TMC4331\TMC4331_register.py
# Compiled at: 2020-02-06 07:23:02
# Size of source mod 2**32: 4230 bytes
"""
Created on 06.02.2020

@author: JM
"""

class TMC4331_register:
    __doc__ = '\n    Define all registers of the TMC4331.\n    '
    GENERAL_CONF = 0
    REFERENCE_CONF = 1
    START_CONF = 2
    INPUT_FILT_CONF = 3
    SPI_OUT_CONF = 4
    CURRENT_CONF = 5
    SCALE_VALUES = 6
    STEP_CONF = 10
    SPI_STATUS_SELECTION = 11
    EVENT_CLEAR_CONF = 12
    INTR_CONF = 13
    EVENTS = 14
    STATUS = 15
    STP_LENGTH_ADD___DIR_SETUP_TIME = 16
    START_OUT_ADD = 17
    GEAR_RATIO = 18
    START_DELAY = 19
    CLK_GATING_DELAY = 20
    STDBY_DELAY = 21
    FREEWHEEL_DELAY = 22
    VDRV_SCALE_LIMIT___PWM_VMAX = 23
    UP_SCALE_DELAY = 24
    HOLD_SCALE_DELAY = 25
    DRV_SCALE_DELAY = 26
    BOOST_TIME = 27
    SPI_SWITCH_VEL___DAC_ADDR = 29
    HOME_SAFETY_MARGIN = 30
    PWM_FREQ___CHOPSYNC_DIV = 31
    RAMPMODE = 32
    XACTUAL = 33
    VACTUAL = 34
    AACTUAL = 35
    VMAX = 36
    VSTART = 37
    VSTOP = 38
    VBREAK = 39
    AMAX = 40
    DMAX = 41
    ASTART = 42
    DFINAL = 43
    DSTOP = 44
    BOW1 = 45
    BOW2 = 46
    BOW3 = 47
    BOW4 = 48
    CLK_FREQ = 49
    POS_COMP = 50
    VIRT_STOP_LEFT = 51
    VIRT_STOP_RIGHT = 52
    X_HOME = 53
    X_LATCH___REV_CNT___X_RANGE = 54
    XTARGET = 55
    X_PIPE0 = 56
    X_PIPE1 = 57
    X_PIPE2 = 58
    X_PIPE3 = 59
    X_PIPE4 = 60
    X_PIPE5 = 61
    X_PIPE6 = 62
    X_PIPE7 = 63
    SH_REG0 = 64
    SH_REG1 = 65
    SH_REG2 = 66
    SH_REG3 = 67
    SH_REG4 = 68
    SH_REG5 = 69
    SH_REG6 = 70
    SH_REG7 = 71
    SH_REG8 = 72
    SH_REG9 = 73
    SH_REG10 = 74
    SH_REG11 = 75
    SH_REG12 = 76
    SH_REG13 = 77
    CLK_Gating___SW_Reset = 79
    FS_VEL___DC_VEL = 96
    DC_TIME___DC_SG___DC_BLKTIME = 97
    DC_LSPTM = 98
    VSTALL_LIMIT = 103
    COVER_LOW___POLLING_STATUS = 108
    COVER_HIGH___POLLING_REG = 109
    COVER_DRV_LOW = 110
    COVER_DRV_HIGH = 111
    MSLUT__ = 112
    MSLUTSEL = 120
    MSCNT___MSOFFSET = 121
    CURRENTA_B = 122
    CURRENTA_B_SPI___TZEROWAIT = 123
    SCALE_PARAM___CIRCULAR_DEC = 124
    START_SIN______DAC_OFFSET = 126
    VERSION_NO = 127