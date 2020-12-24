# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/imagescanner/utils/logger.py
# Compiled at: 2011-05-14 11:42:19
"""Logging related stufff.

$Id: logger.py,v b0e8e4bd3d27 2011/05/14 17:42:19 seocam $"""
import logging
from imagescanner import settings

class CustomStreamHandler(logging.StreamHandler, object):

    def emit(self, record):
        record.msg = '%s: %s' % (record.levelname, record.msg)
        super(CustomStreamHandler, self).emit(record)


def config_logger():
    handler = CustomStreamHandler()
    logging.root.setLevel(settings.LOGGING_LEVEL)
    logging.root.addHandler(handler)