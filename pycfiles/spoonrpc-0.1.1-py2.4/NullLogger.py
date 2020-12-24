# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/spoon/nulllogger.py
# Compiled at: 2006-11-19 22:31:31


class NullLogger(object):
    """
    Dummy logging object.  Doesn't do anything.
    """
    __module__ = __name__

    def debug(self, msg, *args, **kwargs):
        pass

    def info(self, msg, *args, **kwargs):
        pass

    def warning(self, msg, *args, **kwargs):
        pass

    def error(self, msg, *args, **kwargs):
        pass

    def critical(self, msg, *args, **kwargs):
        pass

    def log(self, lvl, msg, *args, **kwargs):
        pass

    def exception(self, msg, *args):
        pass