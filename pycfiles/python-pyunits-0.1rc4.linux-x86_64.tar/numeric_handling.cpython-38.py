# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/hostedtoolcache/Python/3.8.0/x64/lib/python3.8/site-packages/pyunits/numeric_handling.py
# Compiled at: 2019-11-23 19:40:19
# Size of source mod 2**32: 3940 bytes
from typing import Any, Callable
import functools, inspect
from loguru import logger
import numpy as np
from .types import Numeric
from .unitless import Unitless

class WrapNumeric:
    __doc__ = '\n    A decorator that handles automatically converting raw numeric types passed\n    as arguments to Unitless instances. This allows us to simplify code that\n    can accept raw numeric values, because we no longer have to do annoying\n    type checks.\n\n    For example, we can wrap a function like so:\n    @WrapNumeric("foo")\n    def my_awesome_function(foo: Unitless, bar: int) -> None:\n        # Code here.\n\n    Once we do that, all these calls will be valid:\n\n    my_awesome_function(Unitless(5), 1)\n    my_awesome_function(3.14, 2)\n    my_awesome_function([1, 2, 3], 3)\n\n    In the latter cases, the first argument will automatically be converted\n    to a Unitless value inside the decorator.\n    '

    def __init__(self, *args: str):
        """
        :param args: The names of all the arguments to the wrapped function
        that can be numeric types.
        """
        self._WrapNumeric__arg_names = frozenset(args)
        self._WrapNumeric__arg_positions = set()

    def __call__(self, to_wrap: Callable) -> Callable:
        """
        Wraps a function.
        :param to_wrap: The function to wrap.
        :return: The wrapped version of the function.
        """
        functools.update_wrapper(self, to_wrap)
        signature = inspect.signature(to_wrap)
        for pos, name in enumerate(signature.parameters.keys()):
            if name in self._WrapNumeric__arg_names:
                logger.debug("Parameter '{}' can be passed as argument {}.", name, pos)
                self._WrapNumeric__arg_positions.add(pos)

            @functools.singledispatch
            def convert_numeric(maybe_numeric: Any) -> Any:
                """
            If passed a raw numeric value, it creates a Unitless instance out
            of it and returns it. Otherwise, it is an identity.
            :param maybe_numeric: The value.
            :return: Either the same value, or a Unitless instance.
            """
                return maybe_numeric

            @convert_numeric.register(np.ndarray)
            @convert_numeric.register(int)
            @convert_numeric.register(float)
            @convert_numeric.register(list)
            @convert_numeric.register(tuple)
            def _(maybe_numeric: Numeric) -> Unitless:
                return Unitless(maybe_numeric)

            def _wrap_numeric_impl(*args, **kwargs):
                """
            The actual wrapper function.
            :param args: The positional arguments to pass to the wrapped
            function.
            :param kwargs: The keyword arguments to pass to the wrapped
            function.
            :return: The return value of the function.
            """
                wrapped_args = []
                for arg_pos, arg in enumerate(args):
                    if arg_pos in self._WrapNumeric__arg_positions:
                        wrapped_args.append(convert_numeric(arg))
                    else:
                        wrapped_args.append(arg)
                else:
                    wrapped_kwargs = {}
                    for arg_name, value in kwargs.items():
                        if arg_name in self._WrapNumeric__arg_names:
                            wrapped_kwargs[arg_name] = convert_numeric(value)
                        else:
                            wrapped_kwargs[arg_name] = value
                    else:
                        return to_wrap(*wrapped_args, **wrapped_kwargs)

            return _wrap_numeric_impl