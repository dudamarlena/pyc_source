# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/autobahntestsuite/choosereactor.py
# Compiled at: 2018-12-17 11:51:20
import sys, json
if 'bsd' in sys.platform or sys.platform.startswith('darwin'):
    try:
        v = sys.version_info
        if v[0] == 1 or v[0] == 2 and v[1] < 6 or v[0] == 2 and v[1] == 6 and v[2] < 5:
            raise Exception('Python version too old (%s)' % sys.version)
        from twisted.internet import kqreactor
        kqreactor.install()
    except Exception as e:
        print '\nWARNING: Running on BSD or Darwin, but cannot use kqueue Twisted reactor.\n\n => %s\n\nTo use the kqueue Twisted reactor, you will need:\n\n  1. Python >= 2.6.5 or PyPy > 1.8\n  2. Twisted > 12.0\n\nNote the use of >= and >.\n\nWill let Twisted choose a default reactor (potential performance degradation).\n' % str(e)

if False and sys.platform in ('win32', ):
    try:
        from twisted.application.reactors import installReactor
        installReactor('iocp')
    except Exception as e:
        print '\nWARNING: Running on Windows, but cannot use IOCP Twisted reactor.\n\n => %s\n\nWill let Twisted choose a default reactor (potential performance degradation).\n' % str(e)

if sys.platform.startswith('linux'):
    try:
        from twisted.internet import epollreactor
        epollreactor.install()
    except Exception as e:
        print '\nWARNING: Running on Linux, but cannot use Epoll Twisted reactor.\n\n => %s\n\nWill let Twisted choose a default reactor (potential performance degradation).\n' % str(e)