# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\bin\ddp_pvtr.py
# Compiled at: 2015-04-10 09:22:09
import sys
from ddp import *
pvtr = pvtr.PVTR()
if len(sys.argv) == 3:
    if sys.argv[1] == 'gos':
        pvtr.get_origin_slice(sys.argv[2])
    if sys.argv[1] == 'gas':
        pvtr.get_all_slice(sys.argv[2])
    if sys.argv[1] == 'sos':
        pvtr.set_origin_slice(sys.argv[2])
    if sys.argv[1] == 'sas':
        pvtr.set_all_slice(sys.argv[2])
else:
    pvtr.get_origin_slice('x_slice')