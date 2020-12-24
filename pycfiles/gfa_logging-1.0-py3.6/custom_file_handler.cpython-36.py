# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gfa_logging/custom_file_handler.py
# Compiled at: 2018-10-24 09:10:38
# Size of source mod 2**32: 1229 bytes
import os, logging
from logging import handlers

class CustomTimeRotatingFileHandler(logging.handlers.TimedRotatingFileHandler):

    def __init__(self, filename, header, when='midnight', interval=1, backupCount=0, encoding=None, delay=False, utc=True, atTime=None):
        logging.handlers.TimedRotatingFileHandler.__init__(self, filename=filename, when=when, interval=interval,
          backupCount=backupCount,
          encoding=encoding,
          delay=delay,
          utc=utc,
          atTime=atTime)
        self.file_pre_exists = os.path.exists(filename)
        self.header = header
        self.suffix = '%Y%m%d_%H%M'
        self.doRollover()

    def emit(self, record):
        logging.handlers.TimedRotatingFileHandler.emit(self, record)

    def doRollover(self):
        logging.info('Rotating file...')
        logging.handlers.TimedRotatingFileHandler.doRollover(self)
        self.stream.write('{}\n'.format(self.header))