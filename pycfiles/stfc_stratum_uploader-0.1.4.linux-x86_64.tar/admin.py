# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vwa13376/workspace/uploader/archer/projects/admin.py
# Compiled at: 2013-08-12 11:06:04
from django import forms
from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from archer.projects.models import FileSystem, Project

class FileSystemAdminForm(forms.ModelForm):

    class Meta:
        model = FileSystem


class ProjectAdmin(GuardedModelAdmin):
    list_display = ('__unicode__', 'file_system', 'directory')


class FileSystemAdmin(GuardedModelAdmin):
    list_display = ('__unicode__', 'alias', 'mount_point')
    form = FileSystemAdminForm


admin.site.register(FileSystem, admin_class=FileSystemAdmin)
admin.site.register(Project, admin_class=ProjectAdmin)