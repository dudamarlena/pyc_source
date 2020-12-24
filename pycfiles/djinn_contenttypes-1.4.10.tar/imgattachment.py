# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bouma/gitprojects/provgroningen/buildout/src/djinn_contenttypes/djinn_contenttypes/forms/imgattachment.py
# Compiled at: 2014-06-12 11:57:00
from django import forms
from djinn_contenttypes.models import ImgAttachment
from djinn_contenttypes.forms.base import MetaFieldsMixin

class ImgAttachmentForm(MetaFieldsMixin, forms.ModelForm):

    class Meta:
        model = ImgAttachment
        fields = ['title']