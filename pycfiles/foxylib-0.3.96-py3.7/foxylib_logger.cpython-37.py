# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/log/foxylib_logger.py
# Compiled at: 2020-01-06 01:07:42
# Size of source mod 2**32: 1440 bytes
import logging, os, sys
from functools import reduce, lru_cache
from foxylib.tools.log.logger_tool import LoggerTool, FoxylibLogFormatter
FILE_PATH = os.path.realpath(__file__)
REPO_DIR = reduce(lambda x, f: f(x), [os.path.dirname] * 3, FILE_PATH)

class FoxylibLogger:
    rootname = os.path.basename(REPO_DIR)
    level = logging.DEBUG

    @classmethod
    def rootname_list(cls):
        return [cls.rootname]

    @classmethod
    def func2name(cls, func):
        return LoggerTool.rootname_func2name(cls.rootname, func)

    @classmethod
    def func_level2logger(cls, func, level):
        logger = logging.getLogger(cls.func2name(func))
        logger.setLevel(level)
        return logger

    @classmethod
    def func2logger(cls, func):
        return cls.func_level2logger(func, cls.level)

    @classmethod
    def attach_handler2loggers(cls, handler):
        for rootname in cls.rootname_list():
            logger = logging.getLogger(rootname)
            LoggerTool.add_or_skip_handlers(logger, [handler])

    @classmethod
    @lru_cache(maxsize=2)
    def attach_stderr2loggers(cls, level):
        handler = LoggerTool.handler_formatter2formatted(logging.StreamHandler(sys.stderr), FoxylibLogFormatter.formatter())
        handler.setLevel(level)
        cls.attach_handler2loggers(handler)