# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/edw/logger/config.py
# Compiled at: 2018-03-27 11:18:20
import os, logging
from functools import partial
logger = logging.getLogger('edw.logger')

def is_option_enabled(name, default):
    state = os.environ.get(name, default).lower() in ('true', 'yes', 'on')
    logger.info('Option %s: %s', name, state)
    return state


get_true = partial(is_option_enabled, default='true')
get_false = partial(is_option_enabled, default='false')
LOG_PUBLISHER = get_true('EDW_LOGGER_PUBLISHER')
LOG_ERRORS = get_true('EDW_LOGGER_ERRORS')
LOG_CONTENT = get_true('EDW_LOGGER_CONTENT')
LOG_DB = get_true('EDW_LOGGER_DB')
LOG_CATALOG = get_true('EDW_LOGGER_CATALOG')
LOG_CATALOG_STACK = get_false('EDW_LOGGER_CATALOG_STACK')
LOG_USER_IP = get_false('EDW_LOGGER_USER_IP')
LOG_USER_ID = get_false('EDW_LOGGER_USER_ID')