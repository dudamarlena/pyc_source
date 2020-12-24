# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/secobj/utils.py
# Compiled at: 2012-08-15 09:28:12
from secobj.logger import getlogger

def error(ex, log, msg, *args, **kwargs):
    msg = msg.format(*args, **kwargs)
    try:
        if isinstance(log, basestring):
            log = getlogger(log)
        if log is not None:
            log.error(msg)
    except ValueError:
        pass

    return ex(msg)