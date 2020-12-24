# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noval/util/logger.py
# Compiled at: 2019-08-16 02:55:35
# Size of source mod 2**32: 1795 bytes
import logging, sys
LEVEL_FATAL = logging.FATAL
LEVEL_ERROR = logging.ERROR
LEVEL_WARN = logging.WARN
LEVEL_INFO = logging.INFO
LEVEL_DEBUG = logging.DEBUG
loggingInitialized = False
NORMAL_IDE_LOG_NAME = 'noval.ide'
DEBUG_IDE_LOG_NAME = 'noval.debug'
DEFAULT_IDE_LOG_NAME = NORMAL_IDE_LOG_NAME

def initLogging(is_debug=False, force=False):
    global DEBUG_IDE_LOG_NAME
    global DEFAULT_IDE_LOG_NAME
    global default_ide_logger
    global loggingInitialized
    if force or not loggingInitialized:
        loggingInitialized = True
        configFile = None
        log_level = logging.INFO
        defaultStream = sys.stdout
        if is_debug:
            log_level = logging.DEBUG
            DEFAULT_IDE_LOG_NAME = DEBUG_IDE_LOG_NAME
            defaultStream = sys.stderr
        handler = logging.StreamHandler(defaultStream)
        handler.setLevel(log_level)
        handler.setFormatter(logging.Formatter('%(asctime)s %(name)s %(levelname)s: %(message)s'))
        logging.getLogger().addHandler(handler)
        logging.getLogger().setLevel(log_level)
        default_ide_logger = logging.getLogger(DEFAULT_IDE_LOG_NAME)
        default_ide_logger.setLevel(log_level)


default_ide_logger = logging.getLogger(DEFAULT_IDE_LOG_NAME)

def get_logger(logger_name=''):
    if logger_name == '' or logger_name == 'root':
        return default_ide_logger
    return logging.getLogger(logger_name)


# global NORMAL_IDE_LOG_NAME ## Warning: Unused global