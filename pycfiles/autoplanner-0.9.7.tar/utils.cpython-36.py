# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/flanker/Developer/Github/AutoPlanner/autoplanner/utils.py
# Compiled at: 2018-01-03 13:13:05
# Size of source mod 2**32: 2459 bytes
import datetime, re
from django.forms import forms
from django.forms.widgets import Input
from django.utils.translation import ugettext as _
__author__ = 'Matthieu Gallet'
timedelta_matcher = re.compile(_('^\\s*((\\d+)\\s*d\\s*|)((\\d{1,2})\\s*:\\s*([0-5]\\d)\\s*(:\\s*([0-5]\\d)\\s*|)|)$'))

class TimeDeltaInput(Input):
    input_type = 'text'
    template_name = 'django/forms/widgets/text.html'


class TimeDeltaField(forms.Field):
    default_validators = []
    widget = TimeDeltaInput

    def to_python(self, value):
        try:
            return str_to_python(value)
        except ValueError:
            return datetime.timedelta(seconds=0)


def str_to_python(value: str):
    """

    >>> str_to_python('45d 12:34') == datetime.timedelta(days=45, hours=12, minutes=34)
    True
    >>> str_to_python('45d 12:34:56') == datetime.timedelta(days=45, hours=12, minutes=34, seconds=56)
    True
    >>> str_to_python('12:34') == datetime.timedelta(hours=12, minutes=34)
    True
    >>> str_to_python('45d') == datetime.timedelta(days=45)
    True

    :param value:
    :return:
    """
    if not value:
        return
    else:
        matcher = timedelta_matcher.match(value)
        if not matcher:
            raise ValueError()
        groups = matcher.groups()
        result = 0
        if groups[1]:
            result += 86400 * int(groups[1])
        if groups[3]:
            result += 3600 * int(groups[3])
        if groups[4]:
            result += 60 * int(groups[4])
        if groups[5]:
            result += int(groups[6])
        return datetime.timedelta(seconds=result)


def python_to_components(value: datetime.timedelta):
    if value is None:
        return (None, None, None)
    else:
        return (
         value.days, value.seconds // 3600, value.seconds % 3600)


def python_to_str(value: datetime.timedelta):
    if value is None:
        return ''
    else:
        seconds = int(value.total_seconds())
        days = seconds // 86400
        seconds -= days * 86400
        hours = seconds // 3600
        seconds -= hours * 3600
        minutes = seconds / 60
        seconds -= minutes * 60
        values = {'d':days,  'h':hours,  'm':minutes,  's':seconds}
        if days:
            if seconds:
                return _('%(d)dd %(h)02d:%(m)02d:%(s)02d') % values
        if days:
            if (minutes, hours) == (0, 0):
                return _('%(d)dd') % values
        if days:
            return _('%(d)dd %(h)02d:%(m)02d') % values
        if seconds:
            return _('%(h)02d:%(m)02d:%(s)02d') % values
        return _('%(h)02d:%(m)02d') % values