# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/areski/projects/django/django-audiofield/audiofield/models.py
# Compiled at: 2018-01-28 10:05:32
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from audiofield.fields import AudioField
try:
    from django.contrib.auth import get_user_model
    User = settings.AUTH_USER_MODEL
except ImportError:
    from django.contrib.auth.models import User

class AudioFile(models.Model):
    """
    This Model describe the Audio used on the platform,
    this allow to upload audio file and configure
    alternate Text2Speech System
    """
    name = models.CharField(max_length=150, blank=False, verbose_name=_('audio name'), help_text=_('audio file label'))
    audio_file = AudioField(upload_to='upload/audiofiles', blank=True, ext_whitelist=('.mp3',
                                                                                      '.wav',
                                                                                      '.ogg'), verbose_name=_('audio file'))
    user = models.ForeignKey(User, verbose_name=_('user'), help_text=_('select user'))
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = (
         (
          'view_audiofile', _('can see Audio Files')),)
        db_table = 'audio_file'
        verbose_name = _('audio file')
        verbose_name_plural = _('audio files')

    def __unicode__(self):
        return '[%s] %s' % (self.id, self.name)

    def save(self):
        super(AudioFile, self).save()

    def audio_file_player(self):
        """audio player tag for admin"""
        if self.audio_file:
            file_url = settings.MEDIA_URL + str(self.audio_file)
            player_string = '<audio src="%s" controls>Your browser does not support the audio element.</audio>' % file_url
            return player_string

    audio_file_player.allow_tags = True
    audio_file_player.short_description = _('audio file player')