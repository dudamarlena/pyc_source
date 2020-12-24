# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/ramjet/tasks/heart.py
# Compiled at: 2017-11-06 21:55:23
# Size of source mod 2**32: 305 bytes
"""Task 示例
"""
from ramjet.settings import logger
from ramjet.engines import ioloop
logger = logger.getChild('tasks.heart')

def bind_task():

    def callback(*args, **kw):
        logger.info('tasks heart!')
        (ioloop.call_later)(60, callback, *args, **kw)

    ioloop.call_later(0, callback)