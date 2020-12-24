# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/debugprint.py
# Compiled at: 2015-09-01 07:17:44
import inspect, sys, os

class DebugPrint(object):

    def __init__(self, f):
        self.f = f

    def write(self, text):
        frame = inspect.currentframe()
        filename = frame.f_back.f_code.co_filename.rsplit(os.sep, 1)[(-1)]
        lineno = frame.f_back.f_lineno
        prefix = '[%s:%s] ' % (filename, lineno)
        if text == os.linesep:
            self.f.write(text)
        else:
            self.f.write(prefix + text)


if not isinstance(sys.stdout, DebugPrint):
    sys.stdout = DebugPrint(sys.stdout)