# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/swails/src/ParmEd/parmed/utils/fortranformat/config.py
# Compiled at: 2017-02-11 08:13:06
# Size of source mod 2**32: 2199 bytes
import sys, os
RET_WRITTEN_VARS_ONLY = False
RET_UNWRITTEN_VARS_NONE = True
G_INPUT_TRIAL_EDS = [
 'F', 'L', 'A']
ALLOW_ZERO_WIDTH_EDS = True
RECORD_SEPARATOR = '\n'
if sys.version_info[0] >= 3:
    PROC_MAXINT = sys.maxsize
else:
    PROC_MAXINT = sys.maxint
PROC_INCL_PLUS = False
PROC_ALLOW_NEG_BOZ = False
PROC_PAD_CHAR = ' '
PROC_NEG_AS_ZERO = True
PROC_SIGN_ZERO = False
PROC_MIN_FIELD_WIDTH = 46
PROC_DECIMAL_CHAR = '.'
G0_NO_BLANKS = False
PROC_NO_LEADING_BLANK = False
PROC_BLANKS_AS_ZEROS = False

def reset():
    global ALLOW_ZERO_WIDTH_EDS
    global G0_NO_BLANKS
    global G_INPUT_TRIAL_EDS
    global PROC_ALLOW_NEG_BOZ
    global PROC_BLANKS_AS_ZEROS
    global PROC_DECIMAL_CHAR
    global PROC_INCL_PLUS
    global PROC_MAXINT
    global PROC_MIN_FIELD_WIDTH
    global PROC_NEG_AS_ZERO
    global PROC_NO_LEADING_BLANK
    global PROC_PAD_CHAR
    global PROC_SIGN_ZERO
    global RET_UNWRITTEN_VARS_NONE
    global RET_WRITTEN_VARS_ONLY
    G_INPUT_TRIAL_EDS = [
     'F', 'L', 'A']
    if sys.version_info[0] >= 3:
        PROC_MAXINT = sys.maxsize
    else:
        PROC_MAXINT = sys.maxint
    RET_WRITTEN_VARS_ONLY = False
    RET_UNWRITTEN_VARS_NONE = True
    PROC_INCL_PLUS = False
    PROC_ALLOW_NEG_BOZ = False
    PROC_PAD_CHAR = ' '
    PROC_NEG_AS_ZERO = True
    PROC_SIGN_ZERO = False
    PROC_MIN_FIELD_WIDTH = 46
    PROC_DECIMAL_CHAR = '.'
    G0_NO_BLANKS = False
    PROC_NO_LEADING_BLANK = False
    PROC_BLANKS_AS_ZEROS = False
    ALLOW_ZERO_WIDTH_EDS = True