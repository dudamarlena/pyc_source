# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\SQLAlchemy_wrap\exceptions\no_table_operator_class_exception.py
# Compiled at: 2019-08-20 12:27:39
# Size of source mod 2**32: 154 bytes


class NoTableOperatorClassException(Exception):

    def __init__(self, ErrorInfo):
        super().__init__(self)
        self.error_info = ErrorInfo