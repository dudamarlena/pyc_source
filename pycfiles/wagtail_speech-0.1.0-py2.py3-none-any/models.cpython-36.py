# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robmoorman/Developer/moori/wagtail-speech/src/wagtailspeech/models.py
# Compiled at: 2017-05-23 07:19:03
# Size of source mod 2**32: 558 bytes
from django.db import models
from django.utils.translation import ugettext as _
from wagtail.wagtailcore.models import Page

class SynthesizeSpeechMixin(models.Model):
    __doc__ = '\n    Mixin class to support synthesize speech functionalities.\n\n    Example:\n        class HomePage(SynthesizeSpeechMixin, Page):\n            def get_speech_text(self):\n                return self.title\n    '
    audio_stream = models.FileField((_('audio stream')), blank=True, null=True)

    class Meta:
        abstract = True

    def get_speech_text(self):
        pass