# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/adrie/Desktop/Programmation/better-exceptions/better_exceptions/log.py
# Compiled at: 2018-01-24 17:26:56
# Size of source mod 2**32: 898 bytes
from __future__ import absolute_import
import sys
from logging import Logger, StreamHandler

def patch():
    import logging
    from . import format_exception
    logging_format_exception = lambda exc_info: ''.join(format_exception(*exc_info))
    if hasattr(logging, '_defaultFormatter'):
        logging._defaultFormatter.format_exception = logging_format_exception
    patchables = [handler() for handler in logging._handlerList if isinstance(handler(), StreamHandler)]
    patchables = [handler for handler in patchables if handler.stream == sys.stderr]
    patchables = [handler for handler in patchables if handler.formatter is not None]
    for handler in patchables:
        handler.formatter.formatException = logging_format_exception


class BetExcLogger(Logger):

    def __init__(self, *args, **kwargs):
        super(BetExcLogger, self).__init__(*args, **kwargs)
        patch()