# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/subaligner/logger.py
# Compiled at: 2020-02-25 13:05:05
# Size of source mod 2**32: 1169 bytes
import logging
from absl import logging as absl_logging
from .singleton import Singleton
absl_logging._warn_preinit_stderr = 0

class Logger(Singleton):
    __doc__ = 'Common logging.'
    VERBOSE = True

    def __init__(self, output_log='output.log'):
        self._Logger__loggers = {}
        self._Logger__output_log = output_log

    def get_logger(self, name):
        if self._Logger__loggers.get(name):
            return self._Logger__loggers.get(name)
        else:
            logger = logging.getLogger(name)
            logger.setLevel(logging.DEBUG if Logger.VERBOSE else logging.INFO)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler = logging.FileHandler(self._Logger__output_log, 'w+')
            logger.propagate = False
            file_handler.setFormatter(formatter)
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            if not logger.handlers:
                logger.addHandler(file_handler)
                logger.addHandler(console_handler)
            self._Logger__loggers[name] = logger
            return logger