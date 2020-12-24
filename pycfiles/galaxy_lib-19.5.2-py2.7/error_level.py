# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/galaxy/tools/parser/error_level.py
# Compiled at: 2018-09-15 08:40:24


class StdioErrorLevel(object):
    NO_ERROR = 0
    LOG = 1
    WARNING = 2
    FATAL = 3
    FATAL_OOM = 4
    MAX = 4
    descs = {NO_ERROR: 'No error', 
       LOG: 'Log', 
       WARNING: 'Warning', 
       FATAL: 'Fatal error', 
       FATAL_OOM: 'Out of memory error'}

    @staticmethod
    def desc(error_level):
        err_msg = 'Unknown error'
        if error_level > 0 and error_level <= StdioErrorLevel.MAX:
            err_msg = StdioErrorLevel.descs[error_level]
        return err_msg