# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hectorlopez/.virtualenvs/lingotek36/lib/python3.6/site-packages/ltk/logger.py
# Compiled at: 2019-11-20 16:41:05
# Size of source mod 2**32: 1807 bytes
import logging
API_LOG_LEVEL = 15
logging.addLevelName(API_LOG_LEVEL, 'API')
API_RESPONSE_LOG_LEVEL = 12
logging.addLevelName(API_RESPONSE_LOG_LEVEL, 'API Response')

def log_api(self, message, *args, **kwargs):
    if self.isEnabledFor(API_LOG_LEVEL):
        (self._log)(API_LOG_LEVEL, message, args, **kwargs)
        handler = logger.handlers[0]
        handler.close()


def log_api_response(self, message, *args, **kwargs):
    if self.isEnabledFor(API_RESPONSE_LOG_LEVEL):
        (self._log)(API_RESPONSE_LOG_LEVEL, message, args, **kwargs)


logging.Logger.api_call = log_api
logging.Logger.api_response = log_api_response
logger = logging.getLogger('lib')
logging.getLogger('lib').addHandler(logging.NullHandler())

class CustomFormatter(logging.Formatter):
    default_format = '%(levelname)s: %(message)s'
    info_format = '%(message)s'

    def __init__(self, fmt='%(message)s'):
        logging.Formatter.__init__(self, fmt)

    def format(self, record):
        format_orig = self._fmt
        if record.levelno == logging.INFO:
            self._fmt = CustomFormatter.info_format
        else:
            self._fmt = CustomFormatter.default_format
        result = logging.Formatter.format(self, record)
        self._fmt = format_orig
        return result