# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/kc/code/kevinconway/confpy/confpy/options/numopt.py
# Compiled at: 2019-08-24 21:09:19
__doc__ = b'Classes for creating numeric options.'
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from ..core import compat
from ..core import option

class IntegerOption(option.Option):
    """An option which represents an integer value."""

    def coerce(self, value):
        """Convert text values into integer values.

        Args:
            value (str or int): The value to coerce.

        Raises:
            TypeError: If the value is not an int or string.
            ValueError: If the value is not int or an acceptable value.

        Returns:
            int: The integer value represented.
        """
        if isinstance(value, (compat.long, int)):
            return value
        return int(value)


class FloatOption(option.Option):
    """An option which represents a floating point value."""

    def coerce(self, value):
        """Convert text values into float values.

        Args:
            value (str or float): The value to coerce.

        Raises:
            TypeError: If the value is not a float or string.
            ValueError: If the value is not a float or an acceptable value.

        Returns:
            float: The float value represented.
        """
        if isinstance(value, float):
            return value
        return float(value)