# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/_logger.py
# Compiled at: 2019-12-31 04:08:59
# Size of source mod 2**32: 362 bytes
import logging.config
__all__ = ['log_error', 'log_warning', 'log_debug', 'log_fatal', 'log_info']
import os
logging.config.fileConfig(os.path.dirname(os.path.abspath(__file__)) + '/log.conf')
logger = logging.getLogger('root')
log_error = logger.error
log_warning = logger.warning
log_fatal = logger.critical
log_info = logger.info
log_debug = logger.debug