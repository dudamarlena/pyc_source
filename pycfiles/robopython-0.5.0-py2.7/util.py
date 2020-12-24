# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\robopython\pygatt\util.py
# Compiled at: 2020-03-04 11:05:07
from uuid import UUID

def uuid16_to_uuid(uuid16):
    return UUID('0000%04x-0000-1000-8000-00805F9B34FB' % uuid16)