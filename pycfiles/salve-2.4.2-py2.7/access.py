# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/salve/filesys/access.py
# Compiled at: 2015-11-06 23:45:35
import os
from salve import Enum
access_codes = Enum(R_OK=os.R_OK, W_OK=os.W_OK, X_OK=os.X_OK, F_OK=os.F_OK)