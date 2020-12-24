# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/blotter/log.py
# Compiled at: 2019-06-18 11:38:58
# Size of source mod 2**32: 1326 bytes
import os, logging
LOGGING_ENABLED = os.getenv('LOGGING_ENABLED') == 'Y' or False
VERBOSE = os.getenv('VERBOSE') == 'Y' or False
FILENAME = os.getenv('LOG_LOCATION') or 'blot.log'
LOG_LEVEL = os.getenv('LOG_LEVEL') or 'DEBUG'
if LOGGING_ENABLED:
    try:
        log_level = getattr(logging, LOG_LEVEL)
    except Exception as e:
        print('Invalid log level, defaulting to DEBUG')
        log_level = logging.DEBUG

    logging.basicConfig(level=log_level, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
      datefmt='%m-%d %H:%M',
      filename=FILENAME,
      filemode='w')
    if VERBOSE:
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        console.setFormatter(logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s'))
        logging.getLogger('').addHandler(console)

class Logger:

    def __init__(self, name):
        self.logger = logging.getLogger(name)

    def info(self, msg):
        self.logger.info(msg)

    def warn(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)

    def debug(self, msg):
        self.logger.debug(msg)