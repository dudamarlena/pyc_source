# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pydo/log.py
# Compiled at: 2007-02-15 13:23:36
import logging, sys
logger = logging.getLogger('pydo')
logger.addHandler(logging.StreamHandler(sys.stderr))
debug = logger.debug
error = logger.error
warn = logger.warn
critical = logger.critical
exception = logger.exception
info = logger.info
setLogLevel = logger.setLevel
__all__ = [
 'debug', 'error', 'warn', 'critical', 'exception', 'info', 'setLogLevel']