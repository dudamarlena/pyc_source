# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/areski/projects/django/django-audiofield/audiofield/forms.py
# Compiled at: 2015-08-03 13:05:52
from django import forms
from django.forms.fields import FileField
from django.forms import ModelForm
from audiofield.models import AudioFile
from audiofield.widgets import CustomerAudioFileWidget

class AudioFormField(FileField):
    """
    Field Class to upload audio file
    """

    def clean(self, data, initial=None):
        if data != '__deleted__':
            return super(AudioFormField, self).clean(data, initial)
        else:
            return '__deleted__'


class AdminAudioFileForm(ModelForm):
    """
    This form aims to be used in the django admin, support
    all the features for convertion per default
    """

    class Meta:
        model = AudioFile
        fields = ['name', 'audio_file']


class CustomerAudioFileForm(ModelForm):
    """
    The following form aims to be used on frontend to power
    simple upload of audio files without convertion
    """
    audio_file = forms.FileField(widget=CustomerAudioFileWidget)

    class Meta:
        model = AudioFile
        fields = ['name', 'audio_file']
        exclude = ('user', )