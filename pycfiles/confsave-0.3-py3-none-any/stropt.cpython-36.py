# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/kc/code/kevinconway/confpy/confpy/options/stropt.py
# Compiled at: 2019-08-24 21:09:19
# Size of source mod 2**32: 2802 bytes
__doc__ = 'Classes for creating string options.'
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
import copy, re
from ..core import compat
from ..core import option

class StringOption(option.Option):
    """StringOption"""

    def coerce(self, value):
        """Convert any value into a string value.

        Args:
            value (any): The value to coerce.

        Returns:
            str: The string representation of the value.
        """
        if isinstance(value, compat.basestring):
            return value
        else:
            return str(value)


class PatternOption(option.Option):
    """PatternOption"""

    def __init__(self, pattern=None, *args, **kwargs):
        """Initialize the option with a regex pattern.

        Args:
            pattern (str): The regex pattern to match against.
            *args: Any position arguments required by base classes.
            **kwargs: Any keyword arguments required by base classes.

        Raises:
            ValueError: If a pattern is not given.
            TypeError: If the pattern is not a string.
        """
        (super(PatternOption, self).__init__)(*args, **kwargs)
        if pattern is None:
            raise ValueError('The pattern cannot be None.')
        self._pattern = pattern
        self._re = re.compile(pattern)

    @property
    def pattern(self):
        """Get the pattern being used."""
        return self._pattern

    def coerce(self, value):
        """Convert a value into a pattern matched string value.

        All string values are matched against a regex before they are
        considered acceptable values.

        Args:
            value (any): The value to coerce.

        Raises:
            ValueError: If the value is not an acceptable value.

        Returns:
            str: The pattern matched value represented.
        """
        if not isinstance(value, compat.basestring):
            value = str(value)
        if not self._re.match(value):
            raise ValueError('The value {0} does not match the pattern {1}'.format(value, self.pattern))
        return value

    def __deepcopy__(self, memo):
        """Deep copy an PatternOption.

        This implementation accounts for the regex in the class which cannot
        be deep copied normally.
        """
        new_instance = type(self)(pattern=(self._pattern))
        for key, value in self.__dict__.items():
            if key == '_re':
                pass
            else:
                new_instance.__dict__[key] = copy.deepcopy(value, memo)

        return new_instance