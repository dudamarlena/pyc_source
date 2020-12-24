# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/zo/log/handler.py
# Compiled at: 2020-04-01 22:20:28
# Size of source mod 2**32: 883 bytes
import logging, sys
from loguru import logger as log

class InterceptHandler(logging.Handler):

    def emit(self, record: logging.LogRecord) -> None:
        log_opt = log.opt(depth=7, exception=(record.exc_info))
        log_opt.log(record.levelname, record.getMessage())


LOGGING_LEVEL = logging.DEBUG
logging.basicConfig(handlers=[
 InterceptHandler(level=LOGGING_LEVEL)],
  level=LOGGING_LEVEL)
log.configure(handlers=[{'sink':sys.stderr,  'level':LOGGING_LEVEL}])

def main():
    log.info('123')