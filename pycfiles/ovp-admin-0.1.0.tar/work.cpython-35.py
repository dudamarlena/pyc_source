# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/gpa-ovp/django-ovp-admin/ovp_admin/modules/project/work.py
# Compiled at: 2017-01-10 11:12:37
# Size of source mod 2**32: 598 bytes
from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _
from ovp_projects.models import Work

class WorkAdmin(admin.ModelAdmin):
    fields = [
     ('id', 'project'),
     'weekly_hours',
     'description',
     'can_be_done_remotely']
    list_display = [
     'id', 'project', 'weekly_hours', 'can_be_done_remotely']
    list_filter = []
    list_editable = [
     'can_be_done_remotely']
    search_fields = [
     'project__name', 'project__organization__name']
    readonly_fields = [
     'id']
    raw_id_fields = []


admin.site.register(Work, WorkAdmin)