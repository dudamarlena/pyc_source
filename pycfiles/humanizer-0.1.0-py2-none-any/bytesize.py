# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/grimen/Dev/Private/python-humanizer/humanizer/bytesize.py
# Compiled at: 2019-05-15 01:28:34
import rootpath
rootpath.append()
from humanizer.base import Humanizer, HumanizerError
import re
DEFAULT_HUMANIZER_SILENT = False
DEFAULT_HUMANIZER_EXPAND = False
DEFAULT_HUMANIZER_LETTERCASE = 'default'
DEFAULT_HUMANIZER_SPACE = True
DEFAULT_HUMANIZER_UNIT = 'b'
BYTESIZE_UNITS = [
 'b',
 'kb',
 'mb',
 'gb',
 'tb']
BYTESIZE_UNITS_FORMATTED = [
 'B',
 'kB',
 'MB',
 'GB',
 'TB']
BYTESIZE_UNITS_LABELS = [
 'byte',
 'kilobyte',
 'megabyte',
 'gigabyte',
 'terabyte']
BYTESIZE_UNIT_VALUE_MAP = {'b': 1, 
   'kb': 1024, 
   'mb': 1048576, 
   'gb': 1073741824, 
   'tb': 1099511627776}
BYTESIZE_UNIT_LABEL_MAP = {'b': 'byte', 
   'kb': 'kilobyte', 
   'mb': 'megabyte', 
   'gb': 'gigabyte', 
   'tb': 'terabyte'}
BYTESIZE_LABELS = BYTESIZE_UNIT_LABEL_MAP.values()
BYTESIZE_STRING_PARSE_PATTERN = ('({0})\\s*({1})?').format('[0-9.]+', ('|').join(BYTESIZE_UNITS))

def _enumerate_reversed(_list):
    for index in reversed(range(len(_list))):
        yield (
         index, _list[index])


class BytesizeHumanizer(Humanizer):

    def __init__(self, unit=None, expand=None, lettercase=None, space=None):
        super(BytesizeHumanizer, self)
        self.unit = unit or DEFAULT_HUMANIZER_UNIT
        self.expand = expand or DEFAULT_HUMANIZER_EXPAND
        self.lettercase = lettercase or DEFAULT_HUMANIZER_LETTERCASE
        self.space = space or DEFAULT_HUMANIZER_SPACE

    def value(self, value=None):
        units = BYTESIZE_UNITS
        units_labels = BYTESIZE_UNITS_LABELS
        unit_bytes_unit_map = BYTESIZE_UNIT_VALUE_MAP
        value_unit_pattern = BYTESIZE_STRING_PARSE_PATTERN
        try:
            if value is None:
                return 0
            else:
                _value = str(value).lower()
                for index, unit in _enumerate_reversed(units):
                    _unit = units[index]
                    _unit_plural = ('{}s').format(_unit)
                    _unit_label = units_labels[index]
                    _unit_label_plural = ('{}s').format(_unit_label)
                    _value = _value.replace(_unit_label_plural, _unit_label)
                    _value = _value.replace(_unit_label, _unit)

                size_value_unit_pattern = re.match(value_unit_pattern, _value, re.IGNORECASE)
                result = size_value_unit_pattern and size_value_unit_pattern.groups()
                if result is None or len(result) <= 0:
                    raise HumanizerError(('Expected valid number (`<value:int|float>`) or string (`"<value:int|float> <unit:string>"`) but got value `{0}` ({1})').format(value, type(value)), details={'value': value, 
                       'result': result})
                size_value = dict(enumerate(result)).get(0)
                size_unit = dict(enumerate(result)).get(1)
                _bytes = 0
                if size_value:
                    _bytes = float(size_value)
                    if size_unit:
                        size_unit = size_unit.lower()
                        unit_bytes = unit_bytes_unit_map[size_unit]
                        _bytes = _bytes * unit_bytes
                _bytes = int(round(_bytes))
                return _bytes

        except Exception as error:
            raise HumanizerError(error, details={'value': value})

        return

    def human(self, value=None, unit=None, expand=None, lettercase=None, space=None):
        unit = unit or self.unit
        expand = expand or self.expand
        lettercase = lettercase or self.lettercase
        space = space or self.space
        units = BYTESIZE_UNITS
        units_formatted = BYTESIZE_UNITS_FORMATTED
        units_labels = BYTESIZE_UNITS_LABELS
        unit_value_map = BYTESIZE_UNIT_VALUE_MAP
        unit_label_map = BYTESIZE_UNIT_LABEL_MAP
        try:
            if value is None:
                return
            else:
                _value = value
                if isinstance(value, str):
                    _value = self.value(_value)
                _value = float(_value)
                if unit == 'auto':
                    raise NotImplementedError('Not implemented yet')
                else:
                    _unit = (unit or DEFAULT_HUMANIZER_UNIT).lower()
                    _unit_size = float(unit_value_map[_unit])
                    _value = _value / _unit_size
                if _value < 0:
                    raise HumanizerError(('Expected `value >= 0`, but was `{0}`').format(_value), details={'value': _value})
                if _value >= float('inf'):
                    raise HumanizerError(('Expected `value < ∞`, but was `{0}`').format(_value), details={'value': _value})
                if space:
                    separator = ' '
                else:
                    separator = ''
                format_string = '%(value)s %(unit)s'
                if _value.is_integer():
                    _value = int(_value)
                    value_string = format_string % dict(value=_value, unit=_unit)
                else:
                    _value = float('%.1g' % _value)
                    value_string = format_string % dict(value=_value, unit=_unit)
                    value_string = format_string % dict(value=('{0:.10f}').format(_value).rstrip('0'), unit=_unit)
                if expand:
                    for __unit in units:
                        value_string.replace(unit_value_map[__unit], unit_label_map[__unit])

                if 'low' in lettercase or 'down' in lettercase:
                    value_string = value_string.lower()
                elif 'up' in lettercase:
                    value_string = value_string.upper()
                else:
                    value_string = value_string.lower()
                    for index, __unit in _enumerate_reversed(units[1:]):
                        value_string = value_string.replace(units[index], units_formatted[index])

                return value_string

        except Exception as error:
            raise HumanizerError(error, details={'value': value})

        return


def value(*args, **kvargs):
    return BytesizeHumanizer.default().value(*args, **kvargs)


def human(*args, **kvargs):
    return BytesizeHumanizer.default().human(*args, **kvargs)


Humanizer = BytesizeHumanizer
__all__ = [
 'Humanizer',
 'value',
 'human']