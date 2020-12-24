# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\scrapcore\logger.py
# Compiled at: 2017-08-18 10:54:52
# Size of source mod 2**32: 761 bytes
import logging, sys

class Logger:
    level = logging.INFO
    logger = None

    def setup_logger(self, level=logging.INFO):
        """Configure global log settings"""
        if isinstance(level, int):
            self.level = logging.getLevelName(level)
        self.logger = logging.getLogger()
        self.logger.setLevel(self.level)
        if not len(self.logger.handlers):
            ch = logging.StreamHandler(stream=(sys.stderr))
            logformat = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            formatter = logging.Formatter(logformat)
            ch.setFormatter(formatter)
            self.logger.addHandler(ch)

    def get_logger(self):
        return self.logger