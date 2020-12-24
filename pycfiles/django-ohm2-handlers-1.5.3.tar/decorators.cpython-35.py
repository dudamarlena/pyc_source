# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tonra/ohm2/Clients/ohm2/Entwicklung/ohm2-dev/application/website/apps/ohm2_handlers/currencies/decorators.py
# Compiled at: 2016-12-27 16:40:52
# Size of source mod 2**32: 747 bytes
from functools import wraps
from .definitions import CurrenciesInputException
import inspect

def currencies_safe_request(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            frm = inspect.trace()[(-1)]
            ins_filename = frm[1]
            ins_lineno = frm[2]
            ins_function = frm[3]
            if hasattr(e, 'code'):
                code = e.code
            else:
                code = -1
            if hasattr(e, 'message'):
                message = e.message
                extra = ''
            else:
                message = 'Uncaught exception'
                extra = 'Uncaught exception: {0}'.format(e)
            return (None, CurrenciesInputException(code, message, ins_filename, ins_lineno, ins_function, extra=extra))
        else:
            return (
             result, None)

    return wrapper