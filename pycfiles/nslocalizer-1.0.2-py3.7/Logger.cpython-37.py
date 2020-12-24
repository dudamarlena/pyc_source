# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nslocalizer/Helpers/Logger.py
# Compiled at: 2019-02-23 14:43:18
# Size of source mod 2**32: 4891 bytes
import logging

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances.keys():
            cls._instances[cls] = (super(Singleton, cls).__call__)(*args, **kwargs)
        return cls._instances[cls]


RESET_SEQ = '\x1b[0m'
BOLD_SEQ = '\x1b[1m'
COLORS = {'BLACK':'\x1b[1;30m', 
 'RED':'\x1b[1;31m', 
 'GREEN':'\x1b[1;32m', 
 'YELLOW':'\x1b[1;33m', 
 'BLUE':'\x1b[1;34m', 
 'MAGENTA':'\x1b[1;35m', 
 'CYAN':'\x1b[1;36m', 
 'WHITE':'\x1b[1;37m'}
LEVELS = {'WARNING':COLORS['YELLOW'], 
 'INFO':COLORS['BLACK'], 
 'DEBUG':COLORS['MAGENTA'], 
 'CRITICAL':COLORS['BLUE'], 
 'ERROR':COLORS['RED']}

class ColoredFormatter(logging.Formatter):

    def __init__(self, msg, use_color=True):
        logging.Formatter.__init__(self, msg)
        self.use_color = use_color

    def format(self, record):
        levelname = record.levelname
        if self.use_color:
            if levelname in LEVELS:
                levelname_color = LEVELS[levelname] + levelname + RESET_SEQ
                record.levelname = levelname_color
        return logging.Formatter.format(self, record)


class Logger(object):
    __metaclass__ = Singleton
    _internal_logger = None
    _debug_logging = False
    _use_ansi_codes = False

    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def enableDebugLogger(is_debug_logger=False):
        Logger._debug_logging = is_debug_logger

    @staticmethod
    def disableANSI(disable_ansi=False):
        Logger._use_ansi_codes = not disable_ansi

    @staticmethod
    def setupLogger():
        Logger._internal_logger = logging.getLogger('com.pewpewthespells.py.logging_helper')
        level = logging.DEBUG if Logger._debug_logging else logging.INFO
        Logger._internal_logger.setLevel(level)
        handler = logging.StreamHandler()
        handler.setLevel(level)
        formatter = None
        if Logger._debug_logging is True:
            formatter = ColoredFormatter('[%(levelname)s][%(filename)s:%(lineno)s]: %(message)s', Logger._use_ansi_codes)
        else:
            formatter = ColoredFormatter('[%(levelname)s]: %(message)s', Logger._use_ansi_codes)
        handler.setFormatter(formatter)
        Logger._internal_logger.addHandler(handler)

    @staticmethod
    def isVerbose(verbose_logging=False):
        if Logger._internal_logger is None:
            Logger.setupLogger()
        if not verbose_logging:
            Logger._internal_logger.setLevel(logging.WARNING)

    @staticmethod
    def isSilent(should_quiet=False):
        if Logger._internal_logger is None:
            Logger.setupLogger()
        if should_quiet:
            logging_filter = logging.Filter(name='com.pewpewthespells.py.logging_helper.shut_up')
            Logger._internal_logger.addFilter(logging_filter)

    @staticmethod
    def write():
        if Logger._internal_logger is None:
            Logger.setupLogger()
        return Logger._internal_logger