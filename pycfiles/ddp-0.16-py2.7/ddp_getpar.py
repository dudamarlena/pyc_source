# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\bin\ddp_getpar.py
# Compiled at: 2015-04-10 09:22:09
import sys
from ddp import *
if len(sys.argv) == 2:
    if sys.argv[1] == '1':
        getpar.get_ddscat_fromfile()
    if sys.argv[1] == '2':
        getpar.get_ddscat_builtin()
    if sys.argv[1] == '3':
        getpar.get_ddpostprocess()
else:
    getpar.get_ddscat_fromfile()