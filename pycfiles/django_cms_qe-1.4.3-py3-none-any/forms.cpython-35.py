# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomas/git/euroix/django-cms-qe/cms_qe_video/forms.py
# Compiled at: 2019-02-04 04:18:45
# Size of source mod 2**32: 608 bytes
from django import forms
from .models import HostingVideoPlayer

class HostingVideoPlayerForm(forms.ModelForm):
    __doc__ = '\n    Adding ids (HTML attributes) to control(checkbox) and video_hosting_service(selection) to process with JS.\n    Script with processing: templates/cms_qe/defaul/video_widget.html\n    '

    class Meta:
        model = HostingVideoPlayer
        fields = '__all__'
        widgets = {'controls': forms.CheckboxInput(attrs={'id': 'django-cms-qe-vimeo-disabled'}), 
         'video_hosting_service': forms.Select(attrs={'id': 'django-cms-qe-hosting-choices'})}