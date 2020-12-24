# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/socialcommerce/apps/photos/forms.py
# Compiled at: 2009-10-31 23:19:40
from django import forms
from datetime import datetime
from django.utils.translation import ugettext_lazy as _
from photos.models import Image

class PhotoUploadForm(forms.ModelForm):

    class Meta:
        model = Image
        exclude = ('member', 'photoset', 'title_slug', 'effect', 'crop_from')

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(PhotoUploadForm, self).__init__(*args, **kwargs)


class PhotoEditForm(forms.ModelForm):

    class Meta:
        model = Image
        exclude = ('member', 'photoset', 'title_slug', 'effect', 'crop_from', 'image')

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(PhotoEditForm, self).__init__(*args, **kwargs)