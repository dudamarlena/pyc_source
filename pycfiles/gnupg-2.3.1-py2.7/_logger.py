# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gnupg/_logger.py
# Compiled at: 2014-10-27 20:48:47
"""Logging module for python-gnupg."""
from __future__ import absolute_import
from __future__ import print_function
from datetime import datetime
from functools import wraps
import logging, sys, os
try:
    from logging import NullHandler
except:

    class NullHandler(logging.Handler):

        def handle(self, record):
            pass


from . import _ansistrm
GNUPG_STATUS_LEVEL = 9

def status(self, message, *args, **kwargs):
    """LogRecord for GnuPG internal status messages."""
    if self.isEnabledFor(GNUPG_STATUS_LEVEL):
        self._log(GNUPG_STATUS_LEVEL, message, args, **kwargs)


@wraps(logging.Logger)
def create_logger(level=logging.NOTSET):
    """Create a logger for python-gnupg at a specific message level.

    :type level: :obj:`int` or :obj:`str`
    :param level: A string or an integer for the lowest level to include in
                  logs.

    **Available levels:**

    ==== ======== ========================================
    int   str     description
    ==== ======== ========================================
    0    NOTSET   Disable all logging.
    9    GNUPG    Log GnuPG's internal status messages.
    10   DEBUG    Log module level debuging messages.
    20   INFO     Normal user-level messages.
    30   WARN     Warning messages.
    40   ERROR    Error messages and tracebacks.
    50   CRITICAL Unhandled exceptions and tracebacks.
    ==== ======== ========================================
    """
    _test = os.path.join(os.path.join(os.getcwd(), 'gnupg'), 'test')
    _now = datetime.now().strftime('%Y-%m-%d_%H%M%S')
    _fn = os.path.join(_test, '%s_test_gnupg.log' % _now)
    _fmt = '%(relativeCreated)-4d L%(lineno)-4d:%(funcName)-18.18s %(levelname)-7.7s %(message)s'
    logging.addLevelName(GNUPG_STATUS_LEVEL, 'GNUPG')
    logging.Logger.status = status
    if level > logging.NOTSET:
        logging.basicConfig(level=level, filename=_fn, filemode='a', format=_fmt)
        logging.logThreads = True
        if hasattr(logging, 'captureWarnings'):
            logging.captureWarnings(True)
        colouriser = _ansistrm.ColorizingStreamHandler
        colouriser.level_map[9] = (None, 'blue', False)
        colouriser.level_map[10] = (None, 'cyan', False)
        handler = colouriser(sys.stderr)
        handler.setLevel(level)
        formatr = logging.Formatter(_fmt)
        handler.setFormatter(formatr)
    else:
        handler = NullHandler()
    log = logging.getLogger('gnupg')
    log.addHandler(handler)
    log.setLevel(level)
    log.info('Log opened: %s UTC' % datetime.ctime(datetime.utcnow()))
    return log