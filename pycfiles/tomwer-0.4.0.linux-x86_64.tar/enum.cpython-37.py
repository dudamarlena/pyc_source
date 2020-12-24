# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/third_party/enum.py
# Compiled at: 2019-12-11 09:05:54
# Size of source mod 2**32: 2670 bytes
"""An :class:`.Enum` class with additional features."""
from __future__ import absolute_import
__authors__ = [
 'T. Vincent']
__license__ = 'MIT'
__date__ = '29/04/2019'
import enum

class Enum(enum.Enum):
    __doc__ = 'Enum with additional class methods.'

    @classmethod
    def from_value(cls, value):
        """Convert a value to corresponding Enum member

        :param value: The value to compare to Enum members
           If it is already a member of Enum, it is returned directly.
        :return: The corresponding enum member
        :rtype: Enum
        :raise ValueError: In case the conversion is not possible
        """
        if isinstance(value, cls):
            return value
        for member in cls:
            if value == member.value:
                return member

        raise ValueError('Cannot convert: %s' % value)

    @classmethod
    def members(cls):
        """Returns a tuple of all members.

        :rtype: Tuple[Enum]
        """
        return tuple((member for member in cls))

    @classmethod
    def names(cls):
        """Returns a tuple of all member names.

        :rtype: Tuple[str]
        """
        return tuple((member.name for member in cls))

    @classmethod
    def values(cls):
        """Returns a tuple of all member values.

        :rtype: Tuple
        """
        return tuple((member.value for member in cls))