# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\reconstruct\protocols\layer3\mtp3.py
# Compiled at: 2010-05-01 15:45:14
"""
Message Transport Part 3 (SS7 protocol stack)
(untested)
"""
from construct import *
mtp3_header = BitStruct('mtp3_header', Nibble('service_indicator'), Nibble('subservice'))