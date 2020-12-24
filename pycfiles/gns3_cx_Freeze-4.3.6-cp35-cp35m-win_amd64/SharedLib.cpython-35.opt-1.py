# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \.\cx_Freeze\initscripts\SharedLib.py
# Compiled at: 2016-04-18 03:12:47
# Size of source mod 2**32: 726 bytes
import encodings, os, sys, warnings
if not hasattr(sys, 'frozen'):
    sys.frozen = True
    sys.path = sys.path[:4]
os.environ['TCL_LIBRARY'] = os.path.join(DIR_NAME, 'tcl')
os.environ['TK_LIBRARY'] = os.path.join(DIR_NAME, 'tk')