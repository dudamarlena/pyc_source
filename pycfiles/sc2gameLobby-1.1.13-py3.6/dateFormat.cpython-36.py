# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sc2gameLobby\dateFormat.py
# Compiled at: 2018-07-09 21:33:28
# Size of source mod 2**32: 555 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import datetime

def now(givenTime=None):
    if givenTime:
        usableTime = datetime.datetime.utcfromtimestamp(givenTime)
    else:
        usableTime = datetime.datetime.utcnow()
    now = usableTime.replace(microsecond=0)
    now = now.isoformat('_').replace(':', '_')
    return now