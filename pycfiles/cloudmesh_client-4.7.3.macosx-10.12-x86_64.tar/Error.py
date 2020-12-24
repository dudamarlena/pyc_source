# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/common/Error.py
# Compiled at: 2017-04-23 10:30:41
import sys, traceback

class Error(object):

    @classmethod
    def msg(cls, error=None, debug=True, trace=True):
        if debug and error is not None:
            print error
        if trace:
            print traceback.format_exc()
        return

    @classmethod
    def traceback(cls, error=None, debug=True, trace=True):
        Error.msg(error=error, debug=debug, trace=trace)

    @classmethod
    def info(cls, msg):
        print msg

    @classmethod
    def warning(cls, msg):
        print msg

    @classmethod
    def debug(cls, msg):
        print msg

    @classmethod
    def exit(cls, msg):
        print msg
        sys.exit()