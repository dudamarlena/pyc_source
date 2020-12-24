# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/skylar/pinax/projects/testoster/apps/events/forms.py
# Compiled at: 2009-08-11 21:57:51
from django import forms
from events.models import Event

class EventForm(forms.ModelForm):
    """ Simple Event with SplitDateTime for jq-ui widgets """
    start = forms.SplitDateTimeField()

    class Meta:
        model = Event
        exclude = ('object_id', 'content_type', 'owner')


class SearchForm(forms.Form):
    terms = forms.CharField(required=False)
    action = forms.CharField(initial='search', widget=forms.HiddenInput)