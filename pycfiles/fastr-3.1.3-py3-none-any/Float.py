# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hachterberg/dev/fastr/fastr/fastr/resources/datatypes/Float.py
# Compiled at: 2018-05-22 04:27:52
import fastr
from fastr.core.version import Version
from fastr.datatypes import ValueType

class Float(ValueType):
    description = 'A floating point value'

    def _validate(self):
        """
        Validate the value of the DataType.

        :return: flag indicating validity of the Float
        :rtype: bool
        """
        if self.value is None:
            return False
        else:
            if isinstance(self.value, float):
                return True
            else:
                return False

            return

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
            self._value = float(value)
        except (ValueError, TypeError):
            self._value = None
            fastr.log.debug(('Not a valid value for a Float ({}), ignoring!').format(value))

        return