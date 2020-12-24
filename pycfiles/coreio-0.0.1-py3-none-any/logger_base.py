# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/coreinit/logger/logger_base.py
# Compiled at: 2015-11-10 03:27:39


class LoggerBase(object):
    """
    Base class for logging service. To enable logger via DEFAULT_LOGGER, the child
    class should be named Logger.
    """

    def configure(self):
        pass

    def debug(self, msg='', exception=None):
        pass

    def info(self, msg='', exception=None):
        pass

    def warning(self, msg='', exception=None):
        pass

    def error(self, msg='', exception=None):
        pass

    def crit(self, msg='', exception=None):
        pass