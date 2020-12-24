# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/ulutil/daemonize.py
# Compiled at: 2014-12-19 21:46:27
import sys, os

def daemonize(stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
    """ Fork the current process as a daemon, redirecting standard file
        descriptors (by default, redirects them to /dev/null).
    """
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError as e:
        sys.stderr.write('fork #1 failed: (%d) %s\n' % (e.errno, e.strerror))
        sys.exit(1)

    os.chdir('/')
    os.umask(0)
    os.setsid()
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError as e:
        sys.stderr.write('fork #2 failed: (%d) %s\n' % (e.errno, e.strerror))
        sys.exit(1)

    for f in (sys.stdout, sys.stderr):
        f.flush()

    si = file(stdin, 'r')
    so = file(stdout, 'a+')
    se = file(stderr, 'a+', 0)
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())