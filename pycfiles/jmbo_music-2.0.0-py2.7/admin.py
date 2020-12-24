# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/music/admin.py
# Compiled at: 2015-04-21 15:32:16
from django import forms
from django.contrib import admin
from jmbo.admin import ModelBaseAdmin
from preferences import preferences
from music.models import AudioEmbed, Album, Credit, CreditOption, Track, TrackContributor, MusicPreferences

class CreditOptionInline(admin.TabularInline):
    model = CreditOption


class MusicPreferencesAdmin(admin.ModelAdmin):
    inlines = [
     CreditOptionInline]


class TrackCreditInlineAdminForm(forms.ModelForm):

    class Meta:
        model = Credit


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