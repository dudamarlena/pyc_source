# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cantools/util/reporting.py
# Compiled at: 2019-08-05 00:35:42
import sys
from datetime import datetime
LOG_FILE = None
ERROR_CB = None
TIME_CBS = {}

def start_timer(tname):
    TIME_CBS[tname] = datetime.now()


def end_timer(tname, msg=''):
    diff = datetime.now() - TIME_CBS[tname]
    log('[timer] Completed in %s |%s| %s' % (diff, msg, tname), important=True)


def set_log(fname):
    global LOG_FILE
    LOG_FILE = open(fname, 'a')


def close_log():
    global LOG_FILE
    if LOG_FILE:
        LOG_FILE.close()
        LOG_FILE = None
    return


def log(msg, level=0, important=False):
    s = '* %s : %s %s' % (datetime.now(), '  ' * level, msg)
    if important:
        s = '\n%s' % (s,)
    if LOG_FILE:
        LOG_FILE.write('%s\n' % (s,))
    print s


def set_error(f):
    global ERROR_CB
    ERROR_CB = f


def error(msg, *lines):
    log('error: %s' % (msg,), important=True)
    for line in lines:
        log(line, 1)

    log('goodbye')
    if ERROR_CB:
        ERROR_CB(msg)
    else:
        sys.exit()