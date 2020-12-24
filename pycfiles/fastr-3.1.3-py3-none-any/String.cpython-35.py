# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hachterberg/dev/fastr/fastr/fastr/resources/datatypes/String.py
# Compiled at: 2017-06-01 08:34:36
# Size of source mod 2**32: 1176 bytes
from fastr.core.version import Version
from fastr.datatypes import ValueType

class String(ValueType):
    description = 'A simple string value'

    def _validate(self):
        """
        Validate the value of the DataType.

        :return: flag indicating validity of the String
        :rtype: bool
        """
        if self.value is None:
            return False
        else:
            if isinstance(self.value, str):
                return True
            return False