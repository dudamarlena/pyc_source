# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/honeynet/beeswarm/beeswarm/shared/misc/time.py
# Compiled at: 2016-11-12 07:38:04
from datetime import datetime

def isoformatToDatetime(timestamp):
    if '.' in timestamp:
        return datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%f')
    else:
        return datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S')