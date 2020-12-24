# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/tests/forms.py
# Compiled at: 2020-04-15 06:20:40
# Size of source mod 2**32: 218 bytes
from __future__ import annotations
from django import forms

class SampleForm(forms.Form):
    a = forms.CharField()
    b = forms.ChoiceField(choices=(('a', 'a'), ('b', 'b')))
    c = forms.CharField(required=True)