# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/areski/projects/django/django-audiofield/audiofield/admin.py
# Compiled at: 2017-04-04 11:31:41
from django.contrib import admin
from audiofield.models import AudioFile
from django.utils.translation import ugettext_lazy as _
import os

class AudioFileAdmin(admin.ModelAdmin):
    """Allows the administrator to view and modify uploaded audio files"""
    list_display = ('id', 'name', 'audio_file_player', 'created_date', 'user')
    ordering = ('id', )
    actions = [
     'custom_delete_selected']

    def custom_delete_selected(self, request, queryset):
        n = queryset.count()
        for i in queryset:
            if i.audio_file:
                if os.path.exists(i.audio_file.path):
                    os.remove(i.audio_file.path)
            i.delete()

        self.message_user(request, _('Successfully deleted %d audio files.') % n)

    custom_delete_selected.short_description = 'Delete selected items'

    def get_actions(self, request):
        actions = super(AudioFileAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions


admin.site.register(AudioFile, AudioFileAdmin)