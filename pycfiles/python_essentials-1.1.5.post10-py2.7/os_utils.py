# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/python_essentials/lib/os_utils.py
# Compiled at: 2015-01-05 21:21:08
import os, sys, check_os, subprocess as sp

def which(pgm):
    """replacement for python3's shutil.which"""
    if os.path.exists(pgm) and os.access(pgm, os.X_OK):
        return pgm
    path = os.getenv('PATH')
    for p in path.split(os.path.pathsep):
        p = os.path.join(p, pgm)
        if os.path.exists(p) and os.access(p, os.X_OK):
            return p


def hostname():
    if check_os.check_linux():
        return sp.check_output(['hostname']).strip().decode('utf-8')
    raise RuntimeError('operating system not supported')


CHECK_JAVA_NOT_SET = 1
CHECK_JAVA_INVALID = 2

def check_java_valid(java_home=os.getenv('JAVA_HOME')):
    """checks that the `JAVA_HOME` environment variable is set, non-empty and points to a valid Java JDK
    @return `None` if the `JAVA_HOME` variable points to a valid Java JDK`, `CHECK_JAVA_NOT_SET` if `JAVA_HOME` isn't set or empty or `CHECK_JAVA_INVALID` if `JAVA_HOME` doesn't point to a valid Java JDK"""
    if java_home is None or java_home == '':
        return CHECK_JAVA_NOT_SET
    if not os.path.exists(java_home):
        return CHECK_JAVA_INVALID
    else:
        java_binary = os.path.join(java_home, 'bin/java')
        if not os.path.exists(java_binary):
            return CHECK_JAVA_INVALID
        return