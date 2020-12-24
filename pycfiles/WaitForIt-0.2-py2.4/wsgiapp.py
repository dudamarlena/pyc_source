# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/waitforit/wsgiapp.py
# Compiled at: 2007-05-28 14:45:54
from waitforit.middleware import WaitForIt

def make_filter(app, global_conf, time_limit='10', poll_time='10'):
    time_limit = float(time_limit)
    poll_time = float(poll_time)
    return WaitForIt(app, time_limit=time_limit, poll_time=poll_time)