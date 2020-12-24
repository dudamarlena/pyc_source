# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jannis/Documents/code/rtr-supercell/supercell/env3/lib/python3.6/site-packages/supercell/logging.py
# Compiled at: 2019-02-13 11:26:58
# Size of source mod 2**32: 1540 bytes
from __future__ import absolute_import, division, print_function, with_statement
import logging
from logging.handlers import TimedRotatingFileHandler
import os, socket

class SupercellLoggingHandler(TimedRotatingFileHandler):
    __doc__ = 'Logging handler for :mod:`supercell` applications.\n    '

    def __init__(self, logfile):
        """Initialize the :class:`TimedRotatingFileHandler`."""
        logfile = logfile % {'pid': os.getpid()}
        TimedRotatingFileHandler.__init__(self, logfile, when='d', interval=1,
          backupCount=10)


class HostnameFormatter(logging.Formatter):
    __doc__ = '\n    Formatter that adds a hostname field to the LogRecord\n    '

    def format(self, record):
        record.hostname = socket.gethostname()
        record = super(HostnameFormatter, self).format(record)
        return record