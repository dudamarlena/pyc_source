# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kakwa/Geek/GitHub/ldapcherry/tests/disable.py
# Compiled at: 2019-02-09 14:25:48
import os

def travis_disabled(f):

    def _decorator(f):
        print 'test has been disabled on travis'

    if 'TRAVIS' in os.environ and os.environ['TRAVIS'] == 'yes':
        return _decorator
    else:
        return f


def slow_disabled(f):

    def _decorator(f):
        print 'test has been disabled by env var LCNOSLOW'

    if 'LCNOSLOW' in os.environ and os.environ['LCNOSLOW'] == 'yes':
        return _decorator
    else:
        return f