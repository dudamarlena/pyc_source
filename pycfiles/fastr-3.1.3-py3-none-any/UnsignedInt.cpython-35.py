# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hachterberg/dev/fastr/fastr/fastr/resources/datatypes/UnsignedInt.py
# Compiled at: 2018-05-22 04:27:52
# Size of source mod 2**32: 1639 bytes
import fastr
from fastr.datatypes import ValueType

class UnsignedInt(ValueType):
    description = 'an unsigned integer value'

    def _validate(self):
        """
        Validate the value of the DataType.

        :return: flag indicating validity of the Int
        :rtype: bool
        """
        if self.value is None:
            return False
        else:
            if isinstance(self.value, int):
                return self.value >= 0
            return False

    @property
    def value(self):
        """
        The value of object instantiation of this DataType.
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        Setter function for value property
        """
        try:
            self._value = int(value)
        except (ValueError, TypeError):
            self._value = None
            fastr.log.debug('Not a valid value for a Int ({}), ignoring!'.format(value))