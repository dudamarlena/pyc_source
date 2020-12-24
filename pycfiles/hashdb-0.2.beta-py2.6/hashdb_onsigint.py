# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hashdb/hashdb_onsigint.py
# Compiled at: 2011-01-06 01:43:08
import signal, sys

def isatty(f):
    try:
        return f.isatty()
    except:
        return False


def _onsignal(signum, frame):
    if isatty(sys.stdout):
        sys.stdout.flush()
        print '\x1b[0K\x1b[?25h\x1b[0m'
    sys.stdout.flush()
    exit(-1)


signal.signal(signal.SIGINT, _onsignal)