# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/chaos/logging.py
# Compiled at: 2014-10-31 10:19:18
__doc__ = '\nHelper functions for working with the Python built-in logging module.\n'
from __future__ import absolute_import
import collections, logging, logging.handlers, os

def get_logger(name=None, level=logging.NOTSET, handlers=None):
    """
        Create a Python logging Logger for the given name. A special case is
        when the name is None, as this will represent the root Logger object.

        When handlers are specified, the currently configured handlers for this name
        are removed, and the specified handlers are set.

        Parameters
        ----------
        name: string
                Name of the Logger to create. Specify None to designate the root Logger.
        level: string
                One of: CRITICAL, ERROR, WARNING, INFO or DEBUG. Alternatively, use the `logging`
                constants: logging.CRITICAL, logging.ERROR, etc.
        handlers: dict
                Keys specifies the handler, value may optionally contain configuration,
                or be specified as None.

                Supported handlers are:
                - console: logging to stdout. Optionally specify a custom Handler using 'handler'.
                - file: logging to a specific file. Specify the file as 'logfile'.
                - syslog: logging to syslog.

                All handlers support custom output formats by specifying a 'format'.
        """
    logger = logging.getLogger(name)
    if name is None:
        name = 'root'
    if handlers is None:
        handlers = []
    logger.setLevel(level)
    if len(handlers) != 0:
        logger.handlers = []
    if 'console' in handlers:
        if not isinstance(handlers['console'], collections.Iterable):
            handlers['console'] = {}
        if 'handler' in handlers['console']:
            strm = handlers['console']['handler']
        else:
            strm = logging.StreamHandler()
        if 'format' in handlers['console']:
            fmt = logging.Formatter(handlers['console']['format'])
        else:
            fmt = logging.Formatter('%(message)s')
        strm.setLevel(level)
        strm.setFormatter(fmt)
        logger.addHandler(strm)
    if 'file' in handlers:
        if not isinstance(handlers['file'], collections.Iterable):
            raise TypeError('file handler config must be a dict')
        if 'logfile' not in handlers['file']:
            raise ValueError('file handler config must contain logfile path name')
        fil = logging.handlers.WatchedFileHandler(handlers['file']['logfile'])
        if 'format' in handlers['file']:
            fmt = logging.Formatter(handlers['file']['format'])
        else:
            fmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fil.setLevel(level)
        fil.setFormatter(fmt)
        logger.addHandler(fil)
    if 'syslog' in handlers:
        if not isinstance(handlers['syslog'], collections.Iterable):
            handlers['syslog'] = {}
        sysl = logging.handlers.SysLogHandler(address='/dev/log', facility=logging.handlers.SysLogHandler.LOG_SYSLOG)
        if 'format' in handlers['syslog']:
            fmt = logging.Formatter(handlers['syslog']['format'])
        else:
            fmt = logging.Formatter('%(name)s[%(process)s] %(levelname)-8s: %(message)s')
        sysl.setLevel(level)
        sysl.setFormatter(fmt)
        logger.addHandler(sysl)
    return logger