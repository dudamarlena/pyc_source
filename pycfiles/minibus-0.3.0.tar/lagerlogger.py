# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dan/Source/minibus/examples/lagerlogger.py
# Compiled at: 2015-09-09 17:19:25
""" A nice logging function for me

import logging
from lagerlogger import LagerLogger 
logger = LagerLogger("mymodule")
logger.console(logging.INFO)

"""
import logging, logging.handlers, os
FATAL = logging.FATAL
ERROR = logging.ERROR
WARNING = logging.WARNING
WARN = logging.WARN
INFO = logging.INFO
DEBUG = logging.DEBUG

class LagerLogger(logging.Logger):
    """ King of Loggers """

    def __init__(self, name, level=None):
        logging.Logger.__init__(self, name, self.__level(level))
        self.formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s', '%Y-%m-%d %H:%M:%S')

    def __level(self, lvl):
        if lvl is not None:
            return lvl
        else:
            return logging.DEBUG

    def console(self, level):
        """ adds a console handler """
        ch = logging.StreamHandler()
        ch.setLevel(self.__level(level))
        ch.setFormatter(self.formatter)
        self.addHandler(ch)

    def logfile(self, level, path=None):
        if path is None:
            path = 'log.log'
        path = os.path.normpath(os.path.expanduser(path))
        try:
            open(path, 'a').close()
            hdlr = logging.handlers.RotatingFileHandler(path, maxBytes=500000, backupCount=5)
            hdlr.setLevel(self.__level(level))
            hdlr.setFormatter(self.formatter)
        except IOError:
            logging.error('Failed to open file %s for logging' % logpath, exc_info=True)
            sys.exit(1)

        self.addHandler(hdlr)
        return