# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: pystk/config/output_log.py
# Compiled at: 2018-05-17 05:18:57
import os, logging, logging.handlers

def init_log(log_path, level=logging.INFO, when='D', backup=7, formate='%(levelname)s: %(asctime)s: %(filename)s:%(lineno)d * %(thread)d %(message)s', datefmt='%m-%d %H:%M:%S'):
    """
    init_log - initialize log module

    Args:
        log_path: Log file path prefix.
            Log data will go to two files: log_path.log and log_path.log.wf
            Any non-exist parent directories will be created automatically
        level: Msg above the level will be displayed
            DEBUG < INFO < WARNING < ERROR < CRITICAL the default value is logging.INFO
        when: How to split the log file by time interval
            'S' : Seconds
            'M' : Minutes
            'H' : Hours
            'D' : Days
            'W' : Week day
            default value: 'D'
        formate: Format of the log
            default format:
            %(levelname)s: %(asctime)s: %(filename)s:%(lineno)d * %(thread)d %(message)s
            INFO: 12-09 18:02:42: log.py:40 * 139814749787872 HELLO WORLD
        backup: How many backup file to keep
            default value: 7
        datefmt: The format of datetime.

    Raises:
        OSError: Fail to create log directories
        IOError: Fail to open log file
    """
    formatter = logging.Formatter(formate, datefmt)
    logger = logging.getLogger()
    logger.setLevel(level)
    directory = os.path.dirname(log_path)
    if not os.path.isdir(directory):
        os.makedirs(directory)
    handler = logging.handlers.TimedRotatingFileHandler(log_path + '.log', when=when, backupCount=backup)
    handler.setLevel(level)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    handler = logging.handlers.TimedRotatingFileHandler(log_path + '.log.wf', when=when, backupCount=backup)
    handler.setLevel(logging.WARNING)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)