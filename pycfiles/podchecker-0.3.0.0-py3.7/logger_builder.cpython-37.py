# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/podchecker/utils/logger_builder.py
# Compiled at: 2019-07-14 06:02:10
# Size of source mod 2**32: 5050 bytes
import logging

class LoggerBuilder(object):
    s_logger: logging.Logger
    msg_only: bool

    @classmethod
    def build(cls, name='default', level=logging.DEBUG, msgOnly=False):

        def _logger(name, level):
            logger = logging.getLogger(name)
            logger.setLevel(level)
            return logger

        builder = cls()
        builder.msg_only = msgOnly
        builder.s_logger = _logger(name, level)
        return builder

    def addConsole(self):
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.s_logger.level)
        console_handler.setFormatter(ConsoleColoredFormatter.standardFormatter(self.msg_only))
        self.s_logger.addHandler(console_handler)
        return self

    def addFile(self, filepath=''):
        if len(filepath) > 0:
            file_handler = logging.FileHandler(filepath)
            file_handler.setLevel(self.s_logger.level)
            file_handler.setFormatter(FileNormalFormatter.standardFormatter(self.msg_only))
            self.s_logger.handlers = [
             file_handler] + self.s_logger.handlers
        return self

    def logger(self):
        return self.s_logger


class ConsoleColoredFormatter(logging.Formatter):

    @classmethod
    def standardFormatter(cls, msgOnly=False):
        if msgOnly:
            fmt = '%(message)s'
        else:
            fmt = '{1}%(asctime)s.%(msecs)03d{0} {2}[%(name)s] %(filename)s:%(lineno)s{0} [%(levelname)s] {3}:{0} %(message)s'.format(kLoggerFore.RESET, kLoggerFore.GREEN, kLoggerFore.CYAN, kLoggerFore.WHITE)
        return ConsoleColoredFormatter(fmt, '%Y-%m-%d %H:%M:%S')

    def format(self, record):
        if record.levelno in Level2ColorMap:
            record.levelname, record.msg = ('{}{}{}'.format(Level2ColorMap[record.levelno], x, kLoggerFore.RESET) for x in (record.levelname, record.msg))
        return super().format(record)


class FileNormalFormatter(logging.Formatter):

    @classmethod
    def standardFormatter(cls, msgOnly=False):
        if msgOnly:
            fmt = '%(message)s'
        else:
            fmt = '%(asctime)s.%(msecs)03d [%(name)s] %(filename)s:%(lineno)s [%(levelname)s] : %(message)s'
        return FileNormalFormatter(fmt, '%Y-%m-%d %H:%M:%S')


LTCSI = '\x1b['

def code_to_chars(code):
    return LTCSI + str(code) + 'm'


class LTCodes(object):

    def __init__(self):
        for name in dir(self):
            if not name.startswith('_'):
                value = getattr(self, name)
                setattr(self, name, code_to_chars(value))


class LTFore(LTCodes):
    RESET = 0
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37


kLoggerFore = LTFore()
Level2ColorMap = {logging.CRITICAL: kLoggerFore.MAGENTA, 
 logging.ERROR: kLoggerFore.RED, 
 logging.WARNING: kLoggerFore.YELLOW, 
 logging.INFO: kLoggerFore.WHITE, 
 logging.DEBUG: kLoggerFore.BLUE}