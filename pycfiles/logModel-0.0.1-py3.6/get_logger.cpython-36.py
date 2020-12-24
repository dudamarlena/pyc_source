# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\log_model\get_logger.py
# Compiled at: 2019-10-21 01:43:17
# Size of source mod 2**32: 1483 bytes
"""
function: Log_Model
args: debug, info, warn, error, critical
three parameters:file_name, console_level, file_level
"""
import logging, logging.handlers, datetime

def getLogger(log_name, **kwargs):
    log_level = kwargs.get('level', None)
    log_file = kwargs.get('file', None)
    if not all([log_level, log_file]):
        raise ValueError('params is wrong.')
    else:
        if log_level == 'critical':
            log_level = logging.CRITICAL
        else:
            if log_level == 'error':
                log_level = logging.ERROR
            else:
                if log_level == 'warn':
                    log_level = logging.WARNING
                else:
                    if log_level == 'info':
                        log_level = logging.INFO
                    else:
                        if log_level == 'debug':
                            log_level = logging.DEBUG
                        else:
                            log_level = logging.NOTSET
    logger = logging.getLogger(log_name)
    logger.setLevel(log_level)
    if not logger.handlers:
        fileHandler = logging.handlers.TimedRotatingFileHandler(log_file, encoding='utf-8', when='midnight', interval=1, backupCount=30, atTime=(datetime.time(0, 0, 0, 0)))
        streamHandler = logging.StreamHandler()
        formatter = logging.Formatter(fmt='%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        fileHandler.setFormatter(formatter)
        streamHandler.setFormatter(formatter)
        logger.addHandler(fileHandler)
        logger.addHandler(streamHandler)
    return logger