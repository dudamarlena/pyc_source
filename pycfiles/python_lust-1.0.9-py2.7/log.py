# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/lust/log.py
# Compiled at: 2013-03-20 20:01:54
import sys, os, time
DEBUG = False
SETUP = False

def setup(log_path, force=False):
    global SETUP
    if force:
        SETUP = False
    if not SETUP:
        with open(log_path, 'a+') as (f):
            f.write('[%s] INFO: Log opened.\n' % time.ctime())
        os.closerange(0, 1024)
        fd = os.open(log_path, os.O_RDWR | os.O_CREAT)
        os.dup2(0, 1)
        os.dup2(0, 2)
        sys.stdout = os.fdopen(fd, 'a+', 0)
        sys.stderr = sys.stdout
        SETUP = True


def warn(msg):
    print '[%s] WARN: %s' % (time.ctime(), msg)


def error(msg):
    print '[%s] ERROR: %s' % (time.ctime(), msg)


def info(msg):
    print '[%s] INFO: %s' % (time.ctime(), msg)


def debug(msg):
    global DEBUG
    if not DEBUG:
        print '[%s] DEBUG: %s' % (time.ctime(), msg)


def set_debug_level(on):
    global DEBUG
    DEBUG = on