# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ben/dev/signalbox/signalbox/select_time_widget.py
# Compiled at: 2014-08-27 19:26:12
import re
from django.forms.extras.widgets import SelectDateWidget
from django.forms.widgets import Widget, Select, MultiWidget
from django.utils.safestring import mark_safe
__all__ = ('SelectTimeWidget', 'SplitSelectDateTimeWidget')
time_pattern = '(\\d\\d?):(\\d\\d)(:(\\d\\d))? *([aApP]\\.?[mM]\\.?)?$'
RE_TIME = re.compile(time_pattern)
HOURS = 0
MINUTES = 1
SECONDS = 3
MERIDIEM = 4

class SelectTimeWidget(Widget):
    """
    A Widget that splits time input into <select> elements.
    Allows form to show as 24hr: <hour>:<minute>:<second>, (default)
    or as 12hr: <hour>:<minute>:<second> <am|pm> 
    
    Also allows user-defined increments for minutes/seconds
    """
    hour_field = '%s_hour'
    minute_field = '%s_minute'
    second_field = '%s_second'
    meridiem_field = '%s_meridiem'
    twelve_hr = False

    def __init__(self, attrs=None, hour_step=None, minute_step=None, second_step=None, twelve_hr=False):
        """
        hour_step, minute_step, second_step are optional step values for
        for the range of values for the associated select element
        twelve_hr: If True, forces the output to be in 12-hr format (rather than 24-hr)
        """
        self.attrs = attrs or {}
        if twelve_hr:
            self.twelve_hr = True
            self.meridiem_val = 'a.m.'
        if hour_step and twelve_hr:
            self.hours = range(1, 13, hour_step)
        elif hour_step:
            self.hours = range(0, 24, hour_step)
        elif twelve_hr:
            self.hours = range(1, 13)
        else:
            self.hours = range(0, 24)
        if minute_step:
            self.minutes = range(0, 60, minute_step)
        else:
            self.minutes = range(0, 60)
        if second_step:
            self.seconds = range(0, 60, second_step)
        else:
            self.seconds = range(0, 60)

    def render(self, name, value, attrs=None):
        try:
            hour_val, minute_val, second_val = value.hour, value.minute, value.second
            if self.twelve_hr:
                if hour_val >= 12:
                    self.meridiem_val = 'p.m.'
                else:
                    self.meridiem_val = 'a.m.'
        except AttributeError:
            hour_val = minute_val = second_val = 0
            if isinstance(value, basestring):
                match = RE_TIME.match(value)
                if match:
                    time_groups = match.groups()
                    hour_val = int(time_groups[HOURS]) % 24
                    minute_val = int(time_groups[MINUTES])
                    if time_groups[SECONDS] is None:
                        second_val = 0
                    else:
                        second_val = int(time_groups[SECONDS])
                    if time_groups[MERIDIEM] is not None:
                        self.meridiem_val = time_groups[MERIDIEM]
                    elif self.twelve_hr:
                        if hour_val >= 12:
                            self.meridiem_val = 'p.m.'
                        else:
                            self.meridiem_val = 'a.m.'
                    else:
                        self.meridiem_val = None

        if self.twelve_hr and self.meridiem_val:
            if self.meridiem_val.lower().startswith('p') and hour_val > 12 and hour_val < 24:
                hour_val = hour_val % 12
        elif hour_val == 0:
            hour_val = 12
        output = []
        if 'id' in self.attrs:
            id_ = self.attrs['id']
        else:
            id_ = 'id_%s' % name
        hour_val = '%.2d' % hour_val
        minute_val = '%.2d' % minute_val
        second_val = '%.2d' % second_val
        hour_choices = [ ('%.2d' % i, '%.2d' % i) for i in self.hours ]
        local_attrs = self.build_attrs(id=self.hour_field % id_)
        select_html = Select(choices=hour_choices).render(self.hour_field % name, hour_val, local_attrs)
        output.append(select_html)
        minute_choices = [ ('%.2d' % i, '%.2d' % i) for i in self.minutes ]
        local_attrs['id'] = self.minute_field % id_
        select_html = Select(choices=minute_choices).render(self.minute_field % name, minute_val, local_attrs)
        output.append(select_html)
        second_choices = [ ('%.2d' % i, '%.2d' % i) for i in self.seconds ]
        local_attrs['id'] = self.second_field % id_
        select_html = Select(choices=second_choices).render(self.second_field % name, second_val, local_attrs)
        output.append(select_html)
        if self.twelve_hr:
            if self.meridiem_val is not None and self.meridiem_val.startswith('p'):
                meridiem_choices = [
                 ('p.m.', 'p.m.'), ('a.m.', 'a.m.')]
            else:
                meridiem_choices = [
                 ('a.m.', 'a.m.'), ('p.m.', 'p.m.')]
            local_attrs['id'] = local_attrs['id'] = self.meridiem_field % id_
            select_html = Select(choices=meridiem_choices).render(self.meridiem_field % name, self.meridiem_val, local_attrs)
            output.append(select_html)
        return mark_safe(('\n').join(output))

    def id_for_label(self, id_):
        return '%s_hour' % id_

    id_for_label = classmethod(id_for_label)

    def value_from_datadict(self, data, files, name):
        h = data.get(self.hour_field % name, 0)
        m = data.get(self.minute_field % name, 0)
        s = data.get(self.second_field % name, 0)
        meridiem = data.get(self.meridiem_field % name, None)
        if meridiem is not None:
            if meridiem.lower().startswith('p') and int(h) != 12:
                h = (int(h) + 12) % 24
            elif meridiem.lower().startswith('a') and int(h) == 12:
                h = 0
        if (int(h) == 0 or h) and m and s:
            return '%s:%s:%s' % (h, m, s)
        else:
            return data.get(name, None)