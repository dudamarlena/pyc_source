# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/tools/extlib/wtf_html5.py
# Compiled at: 2016-03-29 13:01:19
# Size of source mod 2**32: 2112 bytes
from wtforms import TextField
from wtforms import IntegerField as _IntegerField
from wtforms import DecimalField as _DecimalField
from wtforms import DateField as _DateField
from wtforms.widgets import Input

class DateInput(Input):
    __doc__ = '\n    Creates `<input type=date>` widget\n    '
    input_type = 'date'


class NumberInput(Input):
    __doc__ = '\n    Creates `<input type=number>` widget\n    '
    input_type = 'number'


class RangeInput(Input):
    __doc__ = '\n    Creates `<input type=range>` widget\n    '
    input_type = 'range'


class URLInput(Input):
    __doc__ = '\n    Creates `<input type=url>` widget\n    '
    input_type = 'url'


class EmailInput(Input):
    __doc__ = '\n    Creates `<input type=email>` widget\n    '
    input_type = 'email'


class SearchInput(Input):
    __doc__ = '\n    Creates `<input type=search>` widget\n    '
    input_type = 'search'


class TelInput(Input):
    __doc__ = '\n    Creates `<input type=tel>` widget\n    '
    input_type = 'tel'


class SearchField(TextField):
    __doc__ = '\n    **TextField** using **SearchInput** by default\n    '
    widget = SearchInput()


class DateField(_DateField):
    __doc__ = '\n    **DateField** using **DateInput** by default\n    '
    widget = DateInput()


class URLField(TextField):
    __doc__ = '\n    **TextField** using **URLInput** by default\n    '
    widget = URLInput()


class EmailField(TextField):
    __doc__ = '\n    **TextField** using **EmailInput** by default\n    '
    widget = EmailInput()


class TelField(TextField):
    __doc__ = '\n    **TextField** using **TelInput** by default\n    '
    widget = TelInput()


class IntegerField(_IntegerField):
    __doc__ = '\n    **IntegerField** using **NumberInput** by default\n    '
    widget = NumberInput()


class DecimalField(_DecimalField):
    __doc__ = '\n    **DecimalField** using **NumberInput** by default\n    '
    widget = NumberInput()


class IntegerRangeField(_IntegerField):
    __doc__ = '\n    **IntegerField** using **RangeInput** by default\n    '
    widget = RangeInput()


class DecimalRangeField(_DecimalField):
    __doc__ = '\n    **DecimalField** using **RangeInput** by default\n    '
    widget = RangeInput()