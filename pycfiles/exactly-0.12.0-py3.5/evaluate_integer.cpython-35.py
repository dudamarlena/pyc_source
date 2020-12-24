# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/test_case_utils/condition/integer/evaluate_integer.py
# Compiled at: 2019-12-27 10:07:37
# Size of source mod 2**32: 839 bytes
from typing import Optional

class NotAnIntegerException(Exception):

    def __init__(self, value_string: str, python_exception_message: Optional[str]=None):
        self.value_string = value_string
        self.python_exception_message = python_exception_message


def python_evaluate(s: str) -> int:
    """
    :raises NotAnIntegerException
    """
    try:
        val = eval(s)
        if isinstance(val, int):
            return val
        raise NotAnIntegerException(s)
    except SyntaxError as ex:
        raise NotAnIntegerException(s, ex.msg)
    except ValueError as ex:
        raise NotAnIntegerException(s, str(ex))
    except TypeError as ex:
        raise NotAnIntegerException(s, str(ex))
    except NameError as ex:
        raise NotAnIntegerException(s, str(ex))