# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/twsfolders/_logger.py
# Compiled at: 2014-06-24 07:33:03
import logging
_logger = None

def get_logger():
    global _logger
    if _logger is None:
        _logger = logging.getLogger('twsfolders')
        return _logger
    else:
        return _logger
        return


def log_debug(message, context=None):
    if context:
        msg = '%s - %s' % (context, message)
    else:
        msg = message
    get_logger().debug(msg)