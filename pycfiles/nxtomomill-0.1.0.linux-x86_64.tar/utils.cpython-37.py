# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/nxtomomill/utils.py
# Compiled at: 2020-03-06 05:20:13
# Size of source mod 2**32: 4982 bytes
"""An :class:`.Enum` class with additional features."""
from __future__ import absolute_import
__authors__ = [
 'T. Vincent']
__license__ = 'MIT'
__date__ = '29/04/2019'
import enum, sys, typing

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


class FileExtension(Enum):
    H5 = '.h5'
    HDF5 = '.hdf5'
    NX = '.nx'


def get_file_name(file_name, extension, check=True):
    """
    set the given extension

    :param str file_name: name of the file
    :param str extension: extension to give
    :param bool check: if check, already check if the file as one of the
                       '_FileExtension'
    """
    extension = FileExtension.from_value(extension.lower())
    if check:
        for value in FileExtension.values():
            if file_name.lower().endswith(value):
                return file_name

    return file_name + extension.value()


class Progress:
    __doc__ = 'Simple interface for defining advancement on a 100 percentage base'

    def __init__(self, name: str):
        self._name = name
        self.reset()

    def reset(self, max_: typing.Union[(None, int)]=None) -> None:
        """
        reset the advancement to n and max advancement to max_
        :param int max_:
        """
        self._n_processed = 0
        self._max_processed = max_

    def start_process(self) -> None:
        self.set_advancement(0)

    def set_advancement(self, value: int) -> None:
        """

        :param int value: set advancement to value
        """
        length = 20
        block = int(round(length * value / 100))
        blocks_str = '#' * block + '-' * (length - block)
        msg = '\r{0}: [{1}] {2}%'.format(self._name, blocks_str, round(value, 2))
        if value >= 100:
            msg += ' DONE\r\n'
        sys.stdout.write(msg)
        sys.stdout.flush()

    def end_process(self) -> None:
        """Set advancement to 100 %"""
        self.set_advancement(100)

    def set_max_advancement(self, n: int) -> None:
        """

        :param int n: number of steps contained by the advancement. When
        advancement reach this value, advancement will be 100 %
        """
        self._max_processed = n

    def increase_advancement(self, i: int=1) -> None:
        """

        :param int i: increase the advancement of n step
        """
        self._n_processed += i
        advancement = int(float(self._n_processed / self._max_processed) * 100)
        self.set_advancement(advancement)