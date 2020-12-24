# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jmbo_calendar/admin.py
# Compiled at: 2016-03-10 02:18:44
from django.contrib import admin
from django import forms
from jmbo import USE_GIS
from jmbo.admin import ModelBaseAdmin, ModelBaseAdminForm
from jmbo_calendar.models import Calendar, Event

class EventAdminForm(ModelBaseAdminForm):

    def clean(self, *args, **kwargs):
        data = super(EventAdminForm, self).clean(*args, **kwargs)
        if 'start' in data and 'end' in data and data['start'] and data['end'] and data['start'] >= data['end']:
            raise forms.ValidationError("The event's start date needs\n                    to be earlier than its end date")
        if 'repeat_until' in data and 'end' in data and data['repeat_until'] and data['end'] and data['repeat_until'] < data['end'].date():
            raise forms.ValidationError('An event cannot have a repeat\n                    cutoff earlier than the actual event')
        return data


class EventAdmin(ModelBaseAdmin):
    form = EventAdminForm
    list_display = ModelBaseAdmin.list_display + ('start', 'end', 'next', 'repeat',
                                                  'repeat_until')
    if USE_GIS:
        list_display += ('location', )
    list_filter = ('repeat', )

    def get_fieldsets(self, *args, **kwargs):
        """Re-order fields"""
        result = super(EventAdmin, self).get_fieldsets(*args, **kwargs)
        result = list(result)
        fields = list(result[0][1]['fields'])
        for name in ('content', 'start', 'end', 'repeat', 'repeat_until', 'external_link',
                     'calendars'):
            fields.remove(name)
            fields.append(name)

        result[0][1]['fields'] = tuple(fields)
        return tuple(result)


admin.site.register(Calendar, ModelBaseAdmin)
admin.site.register(Event, EventAdmin)