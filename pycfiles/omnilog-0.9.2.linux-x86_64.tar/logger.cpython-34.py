# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.4/dist-packages/omnilog/logger.py
# Compiled at: 2016-03-08 18:23:57
# Size of source mod 2**32: 657 bytes
import logging
from omnilog.strings import Strings

class Logger(object):
    __doc__ = '\n    Wrapper class for logging\n    '

    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(Strings.APP_NAME)
        self.logger.setLevel(logging.INFO)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)

    def emergency(self, message):
        self.logger.emergency(message)