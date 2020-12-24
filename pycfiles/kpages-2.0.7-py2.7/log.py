# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/kpages/log.py
# Compiled at: 2019-01-22 20:15:38
import sys, logging, logging.handlers
MAX_BYTES = 104857600
B_COUNT = 30
LEVELS = {'debug': logging.DEBUG, 'info': logging.INFO, 
   'warning': logging.WARNING, 
   'error': logging.ERROR, 
   'critical': logging.CRITICAL}

class log:
    """
    封装logging类
    >>level 可以输出的最低级别
    >>type    0:输出到前台和文件 1:输出到文件
    """

    def __init__(self, name, level='debug', type=1):
        debug_file = name + '-debug.log'
        error_file = name + '-error.log'
        self.debug_logger = logging.getLogger(debug_file)
        self.error_logger = logging.getLogger(error_file)
        level = LEVELS.get(level, logging.NOTSET)
        self.debug_logger.setLevel(level)
        dfh = logging.handlers.TimedRotatingFileHandler(debug_file, when='midnight', backupCount=B_COUNT)
        efh = logging.handlers.RotatingFileHandler(error_file, maxBytes=MAX_BYTES, backupCount=B_COUNT)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        dfh.setFormatter(formatter)
        efh.setFormatter(formatter)
        self.debug_logger.addHandler(dfh)
        self.error_logger.addHandler(efh)
        if type == 0:
            ch = logging.StreamHandler()
            ch.setFormatter(formatter)
            self.debug_logger.addHandler(ch)
            self.error_logger.addHandler(ch)

    def debug(self, message):
        u"""调试信息"""
        self.debug_logger.debug(message)

    def info(self, message):
        u"""普通消息"""
        self.debug_logger.info(message)

    def error(self, message):
        u"""错误消息"""
        self.error_logger.error(message)


def test():
    argn = len(sys.argv)
    if argn > 2:
        mylog = log('test', sys.argv[1], sys.argv[2])
    elif argn > 1:
        mylog = log('test', sys.argv[1])
    else:
        mylog = log('test')
    print 'Log testing ...'
    mylog.debug('This is a debug message')
    mylog.info('This is an info message')
    mylog.error('This is an error message')


if __name__ == '__main__':
    test()