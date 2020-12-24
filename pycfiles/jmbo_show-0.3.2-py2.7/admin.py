# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/show/admin.py
# Compiled at: 2013-09-27 03:40:37
from django import forms
from django.contrib import admin
from preferences import preferences
from jmbo.admin import ModelBaseAdmin, ModelBaseAdminForm
from show.models import Appearance, Credit, CreditOption, RadioShow, Contributor, ShowPreferences

class CreditOptionInline(admin.TabularInline):
    model = CreditOption


class ShowPreferencesAdmin(admin.ModelAdmin):
    inlines = [
     CreditOptionInline]


class CreditInlineAdminForm(forms.ModelForm):

    class Meta:
        model = Credit


class CreditInline(admin.TabularInline):
    form = CreditInlineAdminForm
    model = Credit


class ShowAdminForm(ModelBaseAdminForm):

    def clean(self, *args, **kwargs):
        data = super(ShowAdminForm, self).clean(*args, **kwargs)
        if 'start' in data and 'end' in data and data['start'] and data['end'] and data['start'] >= data['end']:
            raise forms.ValidationError("The show's start date needs\n                    to be earlier than its end date")
        if 'repeat_until' in data and 'end' in data and data['repeat_until'] and data['end'] and data['repeat_until'] < data['end'].date():
            raise forms.ValidationError('An show cannot have a repeat\n                    cutoff earlier than the actual show')
        return data


class ShowAdmin(ModelBaseAdmin):
    form = ShowAdminForm
    list_display = ModelBaseAdmin.list_display + ('start', 'end', 'next', 'repeat',
                                                  'repeat_until')
    list_filter = ('repeat', )
    inlines = [CreditInline]


class AppearanceInline(admin.TabularInline):
    model = Appearance


class ContributorAdmin(ModelBaseAdmin):
    inlines = [
     AppearanceInline]


admin.site.register(RadioShow, ShowAdmin)
admin.site.register(Contributor, ContributorAdmin)
admin.site.register(ShowPreferences, ShowPreferencesAdmin)