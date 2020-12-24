# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/lib.linux-i686-2.6/m_lib/clock/tstclock.py
# Compiled at: 2016-07-25 12:05:26
"""Define clock() for systems that do not have it"""
from __future__ import print_function
from clock import clock
from time import sleep
print('Testing...')
sleep(3)
print('Clock:', clock())