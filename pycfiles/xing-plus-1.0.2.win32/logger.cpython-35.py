# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Anaconda3\Lib\site-packages\xing\logger.py
# Compiled at: 2016-01-16 19:19:25
# Size of source mod 2**32: 1985 bytes
import logging.handlers

def Logger(name):
    """파일 로그 클래스

        :param name: 로그 이름
        :type name: str

        ::

            log = Logger(__name__)
    """
    log = logging.getLogger(name)
    if LoggerSetting.LEVEL == 'DEBUG':
        fomatter = logging.Formatter('%(asctime)s[%(levelname)s|%(name)s,%(lineno)s] %(message)s')
        loggerLevel = logging.DEBUG
    else:
        fomatter = logging.Formatter('%(asctime)s[%(name)s] %(message)s')
        if LoggerSetting.LEVEL == 'INFO':
            loggerLevel = logging.INFO
        else:
            loggerLevel = logging.ERROR
    log.setLevel(loggerLevel)
    fileHandler = logging.handlers.RotatingFileHandler(LoggerSetting.FILE, maxBytes=1048576 * LoggerSetting.MAX_MBYTE, backupCount=LoggerSetting.BACK_COUNT, encoding='utf-8')
    streamHandler = logging.StreamHandler()
    fileHandler.setFormatter(fomatter)
    streamHandler.setFormatter(fomatter)
    log.addHandler(fileHandler)
    log.addHandler(streamHandler)
    return log


class LoggerSetting:
    __doc__ = '파일 로그 환경을 설정하는 클래스\n\n        ::\n\n            LoggerSetting.LEVEL = "INFO"\n            LoggerSetting.FILE = "logfile.log"\n    '
    LEVEL = 'DEBUG'
    FILE = 'xingplus.log'
    MAX_MBYTE = 10
    BACK_COUNT = 10