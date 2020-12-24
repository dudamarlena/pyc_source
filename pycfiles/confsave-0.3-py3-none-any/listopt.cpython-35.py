# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/kc/code/kevinconway/confpy/confpy/options/listopt.py
# Compiled at: 2019-08-24 21:34:21
# Size of source mod 2**32: 3075 bytes
__doc__ = 'Classes for creating list options.'
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
import copy
from ..core import compat
from ..core import option as opt

class ListOption(opt.Option):
    """ListOption"""

    def __init__(self, option=None, default=None, *args, **kwargs):
        """Initialize the option with an option type.

        Args:
            option (option.Option): The option which is used to validate all
                list options.

        Raises:
            TypeError: If the given option is not an instance of option.Option.
            TypeError: If the default value is set but not an iterable.
        """
        super(ListOption, self).__init__(*args, **kwargs)
        if not isinstance(option, opt.Option):
            raise TypeError('Option must be an option type.')
        self._option = option
        self._default = default if default is not None else ()
        self._value = self.coerce(self._default)

    def coerce(self, values):
        """Convert an iterable of literals to an iterable of options.

        Args:
            values (iterable or string): An iterable of raw values to convert
            into options. If the value is a string is is assumed to be a
            comma separated list and will be split before processing.

        Returns:
            iterable: An iterable of option values initialized with the raw
                values from `values`.

        Raises:
            TypeError: If `values` is not iterable or string.
            TypeError: If the underlying option raises a TypeError.
            ValueError: If the underlying option raises a ValueError.
        """
        if isinstance(values, compat.basestring):
            values = tuple(value.strip() for value in values.split(','))
        opt_iter = tuple(copy.deepcopy(self._option) for value in values)
        for opt_obj, val in compat.zip(opt_iter, values):
            opt_obj.__set__(None, val)

        return opt_iter

    def __get__(self, obj=None, objtype=None):
        """Get the current value of the option.

        Returns:
            iterable: The iterable of values in the option.

            If the value is unset, a default option is defined, and the
            option is not required then the default value will be returned.

        Raises:
            AttributeError: If the value is unset and required.
            TypeError: If the value is not iterable.
        """
        if self.required and self._value is None:
            raise AttributeError('Attempted to access an unset option.')
        value = self._value
        if not self.required and self._value is None:
            value = self.coerce(self._default)
        return (val.__get__(None, None) for val in value)