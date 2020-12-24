# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/breno/Envs/djangoplus/lib/python3.7/site-packages/djangoplus/ui/components/utils/forms.py
# Compiled at: 2019-04-13 15:22:11
# Size of source mod 2**32: 966 bytes
from djangoplus.ui.components import forms
from djangoplus.ui.components.utils import MultiScheduleTable, ScheduleTable

class ScheduleTableForm(forms.Form):
    values = forms.CharField(label='Values', widget=(forms.widgets.HiddenInput()))

    def __init__(self, *args, **kwargs):
        schedule = kwargs.get('initial', {}).pop('schedule', [])
        kwargs['initial']['values'] = ''
        (super().__init__)(*args, **kwargs)
        form_prefix = self.prefix and '{}-'.format(self.prefix) or None
        self.component = MultiScheduleTable(schedule, (self.request), title='Horários', form_prefix=form_prefix)

    def clean_values(self):
        values = self.cleaned_data['values']
        cleaned_values = []
        if values:
            for value in values.split('|'):
                i, interval = value.split('::')
                cleaned_values.append((ScheduleTable.WEEK_DAYS[(int(i) - 1)], interval))

        return cleaned_values