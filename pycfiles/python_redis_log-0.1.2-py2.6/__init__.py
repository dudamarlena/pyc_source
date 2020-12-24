# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/redislog/__init__.py
# Compiled at: 2011-05-26 02:17:55
"""
redislog - a redis logging handler for python

>>> from redislog import handlers, logger
>>> l = logger.RedisLogger('my.logger')
>>> l.addHandler(handlers.RedisHandler.to("my:channel"))
>>> l.info("I like pie!")
>>> l.error("Oh snap", exc_info=True)

Redis clients subscribed to my:channel will get a json log record.

On errors, if exc_info is True, a printed traceback will be included.
"""
__author__ = 'Jed Parsons <jed@jedparsons.com>'
__version__ = (0, 0, 1)
import logging, logger
logging.setLoggerClass(logger.RedisLogger)