# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: f:\django\django-nimble\nimble\forms\fields.py
# Compiled at: 2017-01-15 11:08:07
# Size of source mod 2**32: 367 bytes
from django import forms
from .widgets import ToggleableMarkdownWidget

class ToggledMarkdownxFormField(forms.CharField):

    def __init__(self, *args, **kwargs):
        super(ToggledMarkdownxFormField, self).__init__(*args, **kwargs)
        self.widget = ToggleableMarkdownWidget()