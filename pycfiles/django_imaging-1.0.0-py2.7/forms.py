# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pielgrzym/work/imaging/git/example_project/imaging/forms.py
# Compiled at: 2012-06-06 15:56:17
from django import forms
from imaging.models import Image

class AjaxUploadForm(forms.ModelForm):

    class Meta:
        model = Image
        exclude = ('content_type', 'content_object', 'object_id', 'ordering')