# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kc/code/kevinconway/confpy/confpy/options/numopt.py
# Compiled at: 2019-08-24 21:09:19
"""Classes for creating numeric options."""
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