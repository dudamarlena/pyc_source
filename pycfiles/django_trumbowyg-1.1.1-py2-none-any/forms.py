# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/est/src/django-trumbowyg/trumbowyg/forms.py
# Compiled at: 2017-03-07 08:19:27
from django import forms

class ImageForm(forms.Form):
    image = forms.ImageField()