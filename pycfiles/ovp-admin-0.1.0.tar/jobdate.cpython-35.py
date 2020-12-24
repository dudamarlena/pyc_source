# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/gpa-ovp/django-ovp-admin/ovp_admin/modules/project/jobdate.py
# Compiled at: 2017-01-10 11:12:37
# Size of source mod 2**32: 380 bytes
from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _
from ovp_projects.models import JobDate

class JobDateInline(admin.TabularInline):
    model = JobDate


class JobDateAdmin(admin.ModelAdmin):
    list_display = [
     'id', 'start_date', 'end_date']
    raw_id_fields = ['job']


admin.site.register(JobDate, JobDateAdmin)