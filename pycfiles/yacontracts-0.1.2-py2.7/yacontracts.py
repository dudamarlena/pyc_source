# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/yacontracts.py
# Compiled at: 2016-08-15 19:08:14
"""YAContrac module
"""
import inspect
from types import FunctionType, ListType, TupleType, StringType

def exec_validator(value, validator, error_message):
    """Run validation

    Checks value against validator and returns error_message
    in case of failure as a ValueError
    """
    if not validator(value):
        raise ValueError(error_message)


class yacontract(object):
    """yacontract decorator

        @yacontract(args=[("arg1", check1, error_message1),
                        ("arg2", check2, error_message2)],
                        returns=(checkR, error_messageR))
    """

    def __init__(self, args=[], returns=None):
        """YaContract initialization

        :param args: List of arguments to validate
        :type args: list

        :param returns: Validation to perform on return
        :type returns: tuple

        Examples:
            args:
                [("argument_1", lambda x: x > 0, 'Error, argument_1 < 0 !'),
                ("argument_N", lambda x: isinstance(x, str), 'Error, not str !')]

            returns:
                (lambda x: isinstance(x, int), 'Return has to be an int')
        """
        if not isinstance(args, ListType):
            raise ValueError('args has to be a list')
        if returns is not None and (not isinstance(returns, TupleType) or not len(returns) == 2 or not isinstance(returns[0], FunctionType) or not isinstance(returns[1], StringType)):
            raise ValueError('returns has to be a valid tuple (validator, message)')
        self.__args = args
        self.__returns = returns
        return

    def __call__(self, foo):
        inspected_args = inspect.getargspec(foo).args

        def wrapped_foo(*args, **kwargs):
            for name, validator, error_message in self.__args:
                assert isinstance(name, StringType)
                assert isinstance(validator, FunctionType)
                assert isinstance(error_message, StringType)
                if name in kwargs:
                    exec_validator(kwargs[name], validator, error_message)
                else:
                    arg_index = None
                    try:
                        arg_index = inspected_args.index(name)
                    except ValueError:
                        raise ValueError(('{} is not a valid argument for {}').format(name, foo.__name__))

                    exec_validator(args[arg_index], validator, error_message)

            result = foo(*args, **kwargs)
            if self.__returns:
                exec_validator(result, self.__returns[0], self.__returns[1])
            return result

        return wrapped_foo