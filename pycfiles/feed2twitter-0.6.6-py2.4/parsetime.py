# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/feed2twitter/parsetime.py
# Compiled at: 2008-08-06 16:52:56
import re
from datetime import timedelta
retime = re.compile('([0-9]{2}):([0-5][0-9])')

def parsetime(stime):
    try:
        se = retime.match(stime)
        matches = se.groups()
        delta = timedelta(hours=int(matches[0]), minutes=int(matches[1]))
        return delta.days * 24 * 60 * 60 + delta.seconds
    except:
        raise Exception, 'String format error'