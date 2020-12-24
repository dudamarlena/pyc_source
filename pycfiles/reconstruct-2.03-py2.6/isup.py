# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\reconstruct\protocols\layer4\isup.py
# Compiled at: 2010-05-01 15:45:14
"""
ISDN User Part (SS7 protocol stack)
"""
from construct import *
isup_header = Struct('isup_header', Bytes('routing_label', 5), UBInt16('cic'), UBInt8('message_type'))