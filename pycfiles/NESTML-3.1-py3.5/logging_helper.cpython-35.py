# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pynestml/utils/logging_helper.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 1289 bytes
"""
expression : left=expression (plusOp='+'  | minusOp='-') right=expression
"""
from pynestml.utils.logger import Logger, LoggingLevel
from pynestml.utils.messages import Messages

class LoggingHelper(object):

    @staticmethod
    def drop_missing_type_error(_assignment):
        code, message = Messages.get_type_could_not_be_derived(_assignment.get_expression())
        Logger.log_message(code=code, message=message, error_position=_assignment.get_expression().get_source_position(), log_level=LoggingLevel.ERROR)