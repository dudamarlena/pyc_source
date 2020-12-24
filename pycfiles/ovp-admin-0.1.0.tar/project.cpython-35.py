# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/gpa-ovp/django-ovp-admin/ovp_admin/modules/project/project.py
# Compiled at: 2017-01-10 11:12:37
# Size of source mod 2**32: 1405 bytes
from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _
from ovp_projects.models import Project

class ProjectAdmin(admin.ModelAdmin):
    fields = [
     ('id', 'highlighted'), ('name', 'slug'),
     ('organization', 'owner'),
     ('applied_count', 'max_applies_from_roles'),
     ('published', 'closed', 'deleted'),
     ('published_date', 'closed_date', 'deleted_date'),
     'address',
     'image',
     ('created_date', 'modified_date'),
     'description', 'details',
     'skills', 'causes', 'roles']
    list_display = [
     'id', 'created_date', 'name', 'organization__name', 'applied_count',
     'highlighted', 'published', 'closed', 'deleted']
    list_filter = [
     'created_date',
     'highlighted', 'published', 'closed', 'deleted']
    list_editable = [
     'highlighted', 'published', 'closed']
    search_fields = [
     'name', 'organization__name']
    readonly_fields = [
     'id', 'created_date', 'modified_date', 'published_date', 'closed_date', 'deleted_date']
    raw_id_fields = []

    def organization__name(self, obj):
        return obj.organization.name

    organization__name.short_description = _('Organization')
    organization__name.admin_order_field = 'organization__name'


admin.site.register(Project, ProjectAdmin)