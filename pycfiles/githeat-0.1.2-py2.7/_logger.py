# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/githeat/core/_logger.py
# Compiled at: 2016-07-07 01:11:03
""" Global application logging.

All modules use the same global logging object. No messages will be emitted
until the logger is started.

"""
from __future__ import absolute_import
from logging import getLogger
from logging import Formatter
from logging import Logger
from logging import NullHandler
from logging import StreamHandler
__all__ = ('logger', )

class _Logger(Logger):
    """ Log messages to STDERR.

    """
    LOGFMT = '%(asctime)s;%(levelname)s;%(name)s;%(msg)s'

    def __init__(self, name=None):
        """ Initialize this logger.

        The name defaults to the application name. Loggers with the same name
        refer to the same underlying object. Names are hierarchical, e.g.
        'parent.child' defines a logger that is a descendant of 'parent'.

        """
        super(_Logger, self).__init__(name or __name__.split('.')[0])
        self.addHandler(NullHandler())
        self.active = False

    def start(self, level='WARN'):
        """ Start logging with this logger.

        Until the logger is started, no messages will be emitted. This applies
        to all loggers with the same name and any child loggers.

        Messages less than the given priority level will be ignored. The
        default level is 'WARN', which conforms to the *nix convention that a
        successful run should produce no diagnostic output. Available levels
        and their suggested meanings:

          DEBUG - output useful for developers
          INFO - trace normal program flow, especially external interactions
          WARN - an abnormal condition was detected that might need attention
          ERROR - an error was detected but execution continued
          CRITICAL - an error was detected and execution was halted

        """
        if self.active:
            return
        handler = StreamHandler()
        handler.setFormatter(Formatter(self.LOGFMT))
        self.addHandler(handler)
        self.setLevel(level.upper())
        self.active = True

    def stop(self):
        """ Stop logging with this logger.

        """
        if not self.active:
            return
        self.removeHandler(self.handlers[(-1)])
        self.active = False


logger = _Logger()