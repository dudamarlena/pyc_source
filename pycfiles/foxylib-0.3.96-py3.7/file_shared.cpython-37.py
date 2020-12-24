# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/messenger/slack/events/file_shared.py
# Compiled at: 2020-01-06 01:07:42
# Size of source mod 2**32: 3009 bytes
import logging
from foxylib.tools.log.foxylib_logger import FoxylibLogger

class FileSharedEvent:
    NAME = 'file_shared'

    @classmethod
    def j_event2j_file_list(cls, j_event):
        logger = FoxylibLogger.func_level2logger(cls.j_event2j_file_list, logging.DEBUG)
        logger.debug({'j_event': j_event})
        j_file_list = j_event.get('files', [])
        return j_file_list