# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/powellc/projects/volunteer-coordination/volunteerhub/apps/volunteers/forms.py
# Compiled at: 2014-06-10 15:49:30
from django.core.urlresolvers import reverse
import floppyforms as forms
from .models import Volunteer, Project, Organization

class OrganizationForm(forms.ModelForm):

    class Meta:
        model = Organization

    def get_success_url(self):
        return reverse('dashboard')


class VolunteerForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = Volunteer
        exclude = ['opportunities_completed', 'user']

    def get_success_url(self):
        return reverse('dashboard')


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        exclude = ['organization', 'lead_volunteers']