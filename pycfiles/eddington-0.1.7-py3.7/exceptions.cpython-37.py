# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/eddington/exceptions.py
# Compiled at: 2020-04-04 13:10:47
# Size of source mod 2**32: 636 bytes
from eddington_core import EddingtonException

class InvalidDataFile(EddingtonException):

    def __init__(self, file_name, sheet=None):
        sheet_msg = '' if sheet is None else f' in sheet "{sheet}"'
        msg = f'"{file_name}" has invalid syntax{sheet_msg}.'
        super(InvalidDataFile, self).__init__(msg)


class ColumnsDuplicationError(EddingtonException):

    def __init__(self, columns):
        join_str = ', '.join(columns)
        msg = f"All columns must be different. The following columns are the same: {join_str}"
        super(ColumnsDuplicationError, self).__init__(msg)