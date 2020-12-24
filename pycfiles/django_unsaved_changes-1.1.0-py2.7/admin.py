# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/django_unsaved_changes/admin.py
# Compiled at: 2017-12-19 18:15:32
from django.contrib import admin
from django.conf import settings

class UnsavedChangesAdminMixin(object):
    change_form_template = 'admin/django_unsaved_changes/change_form.html'

    def add_unsaved_changes_context(self, extra_context):
        try:
            extra_context['UNSAVED_CHANGES_UNSAVED_CHANGES_ALERT'] = (hasattr(self, 'UNSAVED_CHANGES_UNSAVED_CHANGES_ALERT') or settings).UNSAVED_CHANGES_UNSAVED_CHANGES_ALERT if 1 else self.UNSAVED_CHANGES_UNSAVED_CHANGES_ALERT
        except:
            extra_context['UNSAVED_CHANGES_UNSAVED_CHANGES_ALERT'] = False

        try:
            extra_context['UNSAVED_CHANGES_SUMBITTED_ALERT'] = (hasattr(self, 'UNSAVED_CHANGES_SUMBITTED_ALERT') or settings).UNSAVED_CHANGES_SUMBITTED_ALERT if 1 else self.UNSAVED_CHANGES_SUMBITTED_ALERT
        except:
            extra_context['UNSAVED_CHANGES_SUMBITTED_ALERT'] = False

        try:
            extra_context['UNSAVED_CHANGES_SUBMITTED_OVERLAY'] = (hasattr(self, 'UNSAVED_CHANGES_SUBMITTED_OVERLAY') or settings).UNSAVED_CHANGES_SUBMITTED_OVERLAY if 1 else self.UNSAVED_CHANGES_SUBMITTED_OVERLAY
        except:
            extra_context['UNSAVED_CHANGES_SUBMITTED_OVERLAY'] = False

        try:
            extra_context['UNSAVED_CHANGES_UNSAVED_CHANGES_VISUALS'] = (hasattr(self, 'UNSAVED_CHANGES_UNSAVED_CHANGES_VISUALS') or settings).UNSAVED_CHANGES_UNSAVED_CHANGES_VISUALS if 1 else self.UNSAVED_CHANGES_UNSAVED_CHANGES_VISUALS
        except:
            extra_context['UNSAVED_CHANGES_UNSAVED_CHANGES_VISUALS'] = False

        try:
            extra_context['UNSAVED_CHANGES_PERSISTANT_STORAGE'] = (hasattr(self, 'UNSAVED_CHANGES_PERSISTANT_STORAGE') or settings).UNSAVED_CHANGES_PERSISTANT_STORAGE if 1 else self.UNSAVED_CHANGES_PERSISTANT_STORAGE
        except:
            extra_context['UNSAVED_CHANGES_PERSISTANT_STORAGE'] = False

        extra_context['DEBUG'] = settings.DEBUG
        return extra_context

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context = self.add_unsaved_changes_context(extra_context)
        return super(UnsavedChangesAdminMixin, self).change_view(request, object_id, form_url, extra_context)

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context = self.add_unsaved_changes_context(extra_context)
        return super(UnsavedChangesAdminMixin, self).add_view(request, form_url, extra_context)


class UnsavedChangesAdmin(UnsavedChangesAdminMixin, admin.ModelAdmin):
    pass