# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/asyncee/git/django-cmstemplates/cmstemplates/admin.py
# Compiled at: 2016-02-24 05:13:13
from django.contrib import admin
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from cmstemplates.models import Template, TemplateGroup

class TemplateAdminForm(forms.ModelForm):
    """Form which validates template saving process."""

    def __init__(self, *args, **kwargs):
        super(TemplateAdminForm, self).__init__(*args, **kwargs)
        if getattr(settings, 'CMSTEMPLATES_USE_CODEMIRROR', False):
            from codemirror import CodeMirrorTextarea
            self.fields['content'].widget = CodeMirrorTextarea(mode='htmlmixed', dependencies=('javascript',
                                                                                               'xml',
                                                                                               'css'))

    class Meta:
        model = Template
        fields = [
         'name', 'group', 'weight', 'content', 'is_active',
         'only_for_superuser']


class TemplateGroupAdmin(admin.ModelAdmin):
    list_display = [
     'name', 'description', 'templates_count']
    list_filter = ['name']
    search_fields = ['name', 'description']

    def templates_count(self, obj):
        return obj.templates.count()

    templates_count.short_description = _('Templates count')


class TemplateAdmin(admin.ModelAdmin):
    list_display = [
     '__str__', 'group', 'weight', 'is_active']
    list_editable = [
     'weight', 'is_active']
    list_filter = ['group__name']
    save_on_top = True
    search_fields = ['id', 'group__name', 'weight', 'content']
    form = TemplateAdminForm


admin.site.register(TemplateGroup, TemplateGroupAdmin)
admin.site.register(Template, TemplateAdmin)