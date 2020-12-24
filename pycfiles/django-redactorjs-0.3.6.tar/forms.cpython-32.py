# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tigorc/repo/django-redactorjs/redactor/forms.py
# Compiled at: 2014-05-01 07:45:16
from django import forms

class ImageForm(forms.Form):
    file = forms.ImageField()


class FileForm(forms.Form):
    file = forms.FileField()