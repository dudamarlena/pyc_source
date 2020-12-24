# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/sy/log.py
# Compiled at: 2011-06-14 13:57:16
"""
:synopsis: Logging management

.. todo:: Document log handling

.. moduleauthor: Paul Diaconescu <p@afajl.com>
"""
try:
    import logbook
    from logbook import Logger
    logbook_enabled = True
except ImportError:
    logbook_enabled = False

    class Logger(object):

        def __init__(self, name, level=0):
            self.name = name
            self.level = level

        debug = info = warn = warning = notice = error = exception = critical = log = lambda *a, **kw: None


if logbook_enabled:
    loggers = logbook.LoggerGroup()
    loggers.disabled = True

def _new(name):
    log = Logger(name)
    if logbook_enabled:
        loggers.add_logger(log)
    return log