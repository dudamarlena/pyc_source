# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hachterberg/dev/fastr/fastr/fastr/resources/datatypes/Boolean.py
# Compiled at: 2018-08-22 11:13:49
# Size of source mod 2**32: 3680 bytes
import fastr
from fastr.datatypes import ValueType

class Boolean(ValueType):
    __doc__ = '\n    Datatype representing a boolean\n    '
    description = 'A boolean value (True of False)'

    def __str__(self):
        if self._value is None:
            return ''
        if self.format == 'flag' or self.format is None:
            return {True: '__FASTR_FLAG__TRUE___', False: '__FASTR_FLAG__FALSE__'}[self._value]
        if self.format == 'yn':
            return {True: 'y', False: 'n'}[self._value]
        if self.format == 'yes':
            return {True: 'yes', False: 'no'}[self._value]
        if self.format == 'Yes':
            return {True: 'Yes', False: 'No'}[self._value]
        if self.format == 'YES':
            return {True: 'YES', False: 'NO'}[self._value]
        if self.format == 'numeric':
            return {True: '1', False: '0'}[self._value]
        if self.format == 'string':
            return {True: 'true', False: 'false'}[self._value]
        if self.format == 'String':
            return {True: 'True', False: 'False'}[self._value]
        if self.format == 'STRING':
            return {True: 'TRUE', False: 'FALSE'}[self._value]
        if self.format.startswith('CONST:'):
            if self._value:
                return self.format[6:]
            else:
                return '__FASTR_FLAG__FALSE__'
        else:
            if '|' in self.format:
                options = self.format.split('|', 1)
                options = {True: options[0], False: options[1]}
                return options[self._value]
            else:
                fastr.log.warning('Unknown Boolean format ({}), reverting to flag'.format(self.format))
                return {True: '__FASTR_FLAG__TRUE___', False: '__FASTR_FLAG__FALSE__'}[self._value]

    def _validate(self):
        """
        Validate the value of the DataType.

        :return: flag indicating validity of Boolean
        :rtype: bool
        """
        if self.value is None:
            return False
        else:
            if isinstance(self.value, bool):
                return True
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
        translation_table = {0: False, '0': False, 'false': False, '__fastr_flag__false__': False, 
         1: True, '1': True, 'true': True, '__fastr_flag__true___': True}
        if isinstance(value, str):
            value = str(value.lower())
        if isinstance(value, bool):
            self._value = value
        else:
            if value in translation_table:
                self._value = translation_table[value]
            else:
                self._value = None
                fastr.log.debug('Not a valid value for a Boolean ({}), ignoring!'.format(value))