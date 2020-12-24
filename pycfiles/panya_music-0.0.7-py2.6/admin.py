# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/music/admin.py
# Compiled at: 2011-09-19 04:01:13
from django import forms
from django.contrib import admin
from panya.admin import ModelBaseAdmin
from preferences import preferences
from music.models import AudioEmbed, Album, Credit, MusicCreditOption, Track, TrackContributor, MusicPreferences

class MusicCreditOptionInline(admin.TabularInline):
    model = MusicCreditOption


class MusicPreferencesAdmin(admin.ModelAdmin):
    inlines = [
     MusicCreditOptionInline]


class TrackCreditInlineAdminForm(forms.ModelForm):
    role = forms.ChoiceField(label='Role')

    class Meta:
        model = Credit

    def __init__(self, *args, **kwargs):
        """
        Set role choices to credit options
        """
        role_choices = []
        credit_options = preferences.MusicPreferences.musiccreditoption_set.all()
        for credit_option in credit_options:
            role_choices.append((credit_option.role_priority, credit_option.role_name))

        self.declared_fields['role'].choices = [('', '---------')] + role_choices
        super(TrackCreditInlineAdminForm, self).__init__(*args, **kwargs)


class TrackCreditInline(admin.TabularInline):
    form = TrackCreditInlineAdminForm
    model = Credit


class TrackAdmin(ModelBaseAdmin):
    inlines = (
     TrackCreditInline,)


admin.site.register(Album, ModelBaseAdmin)
admin.site.register(AudioEmbed, ModelBaseAdmin)
admin.site.register(MusicPreferences, MusicPreferencesAdmin)
admin.site.register(Track, TrackAdmin)
admin.site.register(TrackContributor, ModelBaseAdmin)