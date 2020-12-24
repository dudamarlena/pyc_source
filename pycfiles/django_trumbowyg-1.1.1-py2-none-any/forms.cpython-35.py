# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/est/src/django-trumbowyg/trumbowyg/forms.py
# Compiled at: 2017-03-07 08:19:27
# Size of source mod 2**32: 103 bytes
from django import forms

class ImageForm(forms.Form):
    image = forms.ImageField()