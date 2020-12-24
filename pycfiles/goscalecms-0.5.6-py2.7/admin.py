# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/goscale/themes/admin.py
# Compiled at: 2013-01-28 01:09:23
from django.contrib import admin, messages
from models import Theme
from django.conf import settings
from django.utils.translation import ugettext, ugettext_lazy as _
from django.db import models
from django import forms

class ThemeAdminForm(forms.ModelForm):

    class Meta:
        model = Theme

    def clean(self):
        cleaned_data = super(ThemeAdminForm, self).clean()
        name = cleaned_data.get('name')
        theme_file = cleaned_data.get('theme_file')
        if not name and not theme_file:
            raise forms.ValidationError(_('Choose at lease one of "Theme file" or "Name".'))
        return cleaned_data


class ThemeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    list_filter = ('name', )
    filter_horizontal = ('sites', )
    form = ThemeAdminForm


admin.site.register(Theme, ThemeAdmin)
from cms.models import Page
from cms.admin.pageadmin import PageAdmin
from cms.admin.forms import PageAddForm, PageForm
admin.site.unregister(Page)
t = Page._meta.get_field_by_name('template')[0]
template_choices = [ (x, _(y)) for x, y in settings.CMS_TEMPLATES ]
t.choices.extend(template_choices)
admin.site.register(Page, PageAdmin)