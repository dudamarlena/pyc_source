# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/kc/code/kevinconway/confpy/confpy/options/boolopt.py
# Compiled at: 2019-08-24 21:09:19
# Size of source mod 2**32: 1217 bytes
__doc__ = 'Classes for creating boolean options.'
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from ..core import option

class BoolOption(option.Option):
    """BoolOption"""

    def coerce(self, value):
        """Convert text values into boolean values.

        True values are (case insensitive): 'yes', 'true', '1'. False values
        are (case insensitive): 'no', 'false', '0'.

        Args:
            value (str or bool): The value to coerce.

        Raises:
            TypeError: If the value is not a bool or string.
            ValueError: If the value is not bool or an acceptable value.

        Returns:
            bool: The True/False value represented.
        """
        if isinstance(value, bool):
            return value
        else:
            if not hasattr(value, 'lower'):
                raise TypeError('Value is not bool or string.')
            if value.lower() in ('yes', 'true', '1'):
                return True
            if value.lower() in ('no', 'false', '0'):
                return False
        raise ValueError('Could not coerce {0} to a bool.'.format(value))