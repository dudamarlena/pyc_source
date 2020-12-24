# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/kc/code/kevinconway/confpy/confpy/core/option.py
# Compiled at: 2019-08-24 21:09:19
# Size of source mod 2**32: 2580 bytes
__doc__ = 'Classes for creating validated configuration options.'
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

class Option(object):
    """Option"""

    def __init__(self, description=None, default=None, required=False):
        """Initialize the option with some basic metadata.

        Args:
            description (str, optional): A human readable description of what
                the option represents.
            default (optional): The default value to use if unset.
            required (bool, optional): Whether or not the value must be set.
        """
        self.__doc__ = description
        self._default = default
        self._value = default
        self._required = bool(required)

    @property
    def description(self):
        """Get the human description of the options."""
        return self.__doc__

    @property
    def default(self):
        """Get the default value of the property."""
        return self._default

    @property
    def required(self):
        """Get whether or not the value is required."""
        return self._required

    @property
    def value(self):
        """Get the current value of the option.

        If the value is unset the default value will be used instead.
        """
        if self._value is not None:
            return self._value
        return self._default

    @value.setter
    def value(self, val):
        """Set the value of the option.
        Args:
            val: The value to set the option to.

        Raises:
            TypeError: If the value is not a string or appropriate native type.
            ValueError: If the value is a string but cannot be coerced.
        """
        self._value = self.coerce(val)

    def coerce(self, value):
        """Convert a string to the appropriate Python value.

        If the value is already the appropriate Python value it should be
        returned without change.

        Args:
            value (str): The string value to coerce.

        Raises:
            TypeError: If the value is not string or appropriate native type.
            ValueError: If the value cannot be converted.

        Returns:
            object: Some Python value.
        """
        return value

    def __get__(self, obj=None, objtype=None):
        """Proxy the request to the 'value' property."""
        return self.value

    def __set__(self, obj, value):
        """Proxy the request to the 'value' property."""
        self.value = value