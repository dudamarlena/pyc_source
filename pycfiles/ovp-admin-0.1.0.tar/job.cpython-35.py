# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/gpa-ovp/django-ovp-admin/ovp_admin/modules/project/job.py
# Compiled at: 2017-01-10 11:12:37
# Size of source mod 2**32: 474 bytes
from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _
from ovp_projects.models import Job, JobDate
from .jobdate import JobDateAdmin, JobDateInline

class JobAdmin(admin.ModelAdmin):
    exclude = [
     'dates']
    list_display = ['id', 'project', 'start_date', 'end_date']
    search_fields = ['id', 'project__name', 'project__nonprofit__name']
    inlines = (
     JobDateInline,)


admin.site.register(Job, JobAdmin)