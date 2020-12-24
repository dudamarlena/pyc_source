# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /slapdsock/loghelper.py
# Compiled at: 2019-11-11 16:56:42
# Size of source mod 2**32: 2234 bytes
"""
slapd.loghelper - Helper stuff for using logging module

slapdsock - OpenLDAP back-sock listeners with Python
see https://www.stroeder.com/slapdsock.html

(c) 2015-2019 by Michael Stroeder <michael@stroeder.com>

This software is distributed under the terms of the
Apache License Version 2.0 (Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0
"""
import logging
from logging.handlers import SysLogHandler
__all__ = [
 'SYS_LOG_FORMAT',
 'CONSOLE_LOG_FORMAT',
 'combined_logger']
SYS_LOG_FORMAT = '%(levelname)s %(message)s'
CONSOLE_LOG_FORMAT = '%(asctime)s %(levelname)s %(message)s'

def combined_logger(log_name, log_level=logging.INFO, sys_log_format=None, console_log_format=None):
    """
    Returns a combined SysLogHandler/StreamHandler logging instance
    with formatters
    """
    new_logger = logging.getLogger(log_name)
    if sys_log_format:
        my_syslog_formatter = logging.Formatter(fmt=(' '.join((log_name, sys_log_format))))
        my_syslog_handler = logging.handlers.SysLogHandler(address='/dev/log',
          facility=(SysLogHandler.LOG_DAEMON))
        my_syslog_handler.setFormatter(my_syslog_formatter)
        new_logger.addHandler(my_syslog_handler)
    if console_log_format:
        my_stream_formatter = logging.Formatter(fmt=console_log_format)
        my_stream_handler = logging.StreamHandler()
        my_stream_handler.setFormatter(my_stream_formatter)
        new_logger.addHandler(my_stream_handler)
    new_logger.setLevel(log_level)
    return new_logger