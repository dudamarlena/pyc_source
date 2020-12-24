# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\PyTrinamic\ic\TMC4330\TMC4330_register.py
# Compiled at: 2020-02-06 08:37:32
# Size of source mod 2**32: 6225 bytes
"""
Created on 06.02.2020

@author: JM
"""

class TMC4330_register:
    __doc__ = '\n    Define all registers of the TMC4330.\n    '
    GENERAL_CONF = 0
    REFERENCE_CONF = 1
    START_CONF = 2
    INPUT_FILT_CONF = 3
    SCALE_CONF = 5
    ENC_IN_CONF = 7
    ENC_IN_DATA = 8
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
    PWM_VMAX = 23
    CL_ANGLES = 28
    HOME_SAFETY_MARGIN = 30
    PWM_FREQ = 31
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
    ENC_POS = 80
    ENC_LATCH___ENC_RESET_VAL = 81
    ENC_POS_DEV___CL_TR_TOLERANCE = 82
    ENC_POS_DEV_TOL = 83
    ENC_IN_RES___ENC_CONST = 84
    ENC_OUT_RES = 85
    SER_CLK_IN_HIGH_LOW = 86
    SSI_IN_CLK_DELAY___SSI_IN_WTIME = 87
    SER_PTIME = 88
    CL_OFFSET = 89
    PID_VEL___PID_P___CL_VMAX_CALC_P = 90
    PID_ISUM_RD___PID_I___CL_VMAX_CALC_I = 91
    PID_D___CL_DELTA_P = 92
    PID_E___PID_I_CLIP___PID_D_CLKDIV = 93
    PID_DV_CLIP = 94
    PID_TOLERANCE___CL_TOLERANCE = 95
    CL_VMIN_EMF = 96
    CL_VADD_EMF = 97
    ENC_VEL_ZERO = 98
    ENC_VMEAN_SER_ENC_VARIATION_CL_CYCLE = 99
    V_ENC = 101
    V_ENC_MEAN = 102
    ADDR_TO_ENC = 104
    DATA_TO_ENC = 105
    ADDR_FROM_ENC = 106
    DATA_FROM_ENC = 107
    MSLUT__ = 112
    MSLUTSEL = 120
    MSCNT = 121
    USTEPTA_B = 122
    USTEPA_B_SCALE = 123
    CIRCULAR_DEC = 124
    ENC_COMP____ = 125
    START_SIN___ = 126
    VERSION_NO = 127