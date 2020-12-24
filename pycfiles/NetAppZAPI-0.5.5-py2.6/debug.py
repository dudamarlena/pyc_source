# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/netappzapi/debug.py
# Compiled at: 2010-10-08 17:48:52
__version__ = '$Revision: 1.28 $'
import logging, logging.handlers, sys
FORMAT = '%(asctime)s %(levelname)7s: %(message)s'
formatter = logging.Formatter(FORMAT, '%Y-%m-%d %H:%M:%S')
stdoutHandler = logging.StreamHandler(sys.stdout)
stdoutHandler.setFormatter(formatter)

class LocalLogger(logging.Logger):

    def __init__(self, name):
        level = logging.INFO
        logging.Logger.__init__(self, name, level)
        self.addHandler(stdoutHandler)


def add_file_handler(filename):
    handler = logging.handlers.RotatingFileHandler(filename=filename, maxBytes=10000000.0, backupCount=10)
    handler.setFormatter(formatter)
    log = logging.getLogger('zapi')
    log.addHandler(handler)


logging.setLoggerClass(LocalLogger)