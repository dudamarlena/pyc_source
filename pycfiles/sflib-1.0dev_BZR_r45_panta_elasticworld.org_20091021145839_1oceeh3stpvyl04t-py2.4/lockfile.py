# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/sflib/lockfile.py
# Compiled at: 2009-02-25 15:50:34
__author__ = 'Jim Segrave'
__copyright__ = 'Copyright (C) Jim Segrave'
__revision__ = '$Id$'
__version__ = '0.1'
__contributors__ = [
 'Marco Pantaleoni <panta@elasticworld.org>']
import os, errno, sys, time, stat
MAX_WAIT = 10

def get_lock(lockfile, max_wait=0):
    lockdir = os.path.dirname(lockfile)
    if not os.path.exists(lockdir):
        os.mkdir(lockdir, 511)
    while True:
        try:
            fd = os.open(lockfile, os.O_EXCL | os.O_RDWR | os.O_CREAT)
            break
        except OSError, e:
            if e.errno != errno.EEXIST:
                raise

        try:
            f = open(lockfile, 'r')
            s = os.stat(lockfile)
        except OSError, e:
            if e.errno != errno.EEXIST:
                sys.stderr.write('%s exists but stat() failed: %s\n' % (lockfile, e.strerror))
                continue

        if max_wait is not None and max_wait > 0:
            now = int(time.time())
            if now - s[stat.ST_MTIME] > max_wait:
                pid = f.readline()
                sys.stderr.write('%s has been locked for more than %d seconds (PID %s)\n' % (lockfile, max_wait, pid))
                return False
            f.close()
            time.sleep(1)
            continue
        else:
            pid = f.readline()
            sys.stderr.write('%s is locked by PID %s\n' % (lockfile, pid))
            return False

    f = os.fdopen(fd, 'w')
    f.write('%d\n' % os.getpid())
    f.close()
    return True