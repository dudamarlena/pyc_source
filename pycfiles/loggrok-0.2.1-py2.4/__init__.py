# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/loggrok/__init__.py
# Compiled at: 2006-01-04 21:01:57


def getLoggrok():
    import log, actions, parse

    class ModuleSpace:
        __module__ = __name__
        log = log
        actions = actions
        parse = parse

    return ModuleSpace()