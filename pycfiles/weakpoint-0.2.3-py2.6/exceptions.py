# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/weakpoint/exceptions.py
# Compiled at: 2012-11-21 04:46:57


class WeakPointException(Exception):
    code = 1

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return ('{0}').format(self.message)


class OptionException(WeakPointException):
    pass


class RendererException(WeakPointException):
    pass


class ParserException(WeakPointException):
    pass


class ConfigException(WeakPointException):
    pass