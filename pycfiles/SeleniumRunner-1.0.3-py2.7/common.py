# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/sr/common.py
# Compiled at: 2019-03-23 08:40:14
from logger import init_logger
logger = init_logger()

class Common:

    @staticmethod
    def print_loggr(text):

        def decorator(func):

            def wrapper(*args, **kw):
                logger.info(text)
                f = func(*args, **kw)

            return wrapper

        return decorator