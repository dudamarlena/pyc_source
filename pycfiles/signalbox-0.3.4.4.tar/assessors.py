# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ben/dev/signalbox/signalbox/views/assessors.py
# Compiled at: 2014-08-27 19:26:12
from datetime import datetime, timedelta
from django.template import RequestContext, Context, Template
from django.shortcuts import render_to_response, get_object_or_404
from django import forms
from signalbox.models import Observation, Reply, Answer, StudySite
from signalbox.decorators import group_required
import selectable.forms
from registration.forms import RegistrationForm
from signalbox.lookups import UserLookup

class ObservationFilterForm(forms.Form):
    participant = selectable.AutoCompleteSelectField(lookup_class=UserLookup, required=False)
    hide_complete = forms.BooleanField(initial=True, required=False)
    site = forms.ModelChoiceField(queryset=StudySite.objects.all(), required=False)


@group_required(['Researchers', 'Assessors', 'Research Assistants', 'Clinicians'])
def observations_outstanding(request):
    form = ObservationFilterForm(request.POST or None)
    obs_due = Observation.objects.personalised(user=request.user, due_now=True)
    if form.is_valid():
        participant = form.cleaned_data.get('participant', None)
        hide_complete = form.cleaned_data.get('hide_complete', True)
        site = form.cleaned_data.get('site', None)
        if site:
            obs_due = obs_due.filter(dyad__user__userprofile__site=site)
        if participant:
            obs_due = obs_due.filter(dyad__user=participant)
        if hide_complete:
            obs_due = obs_due.exclude(status=1)
    pagedict = {'observation_list': obs_due, 'form': form}
    return render_to_response('admin/signalbox/assessor/observations_due.html', pagedict, context_instance=RequestContext(request))