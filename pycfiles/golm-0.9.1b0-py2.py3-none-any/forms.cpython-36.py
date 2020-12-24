# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/prihodad/Documents/projects/visitor/golm/golm/golm_webgui/forms.py
# Compiled at: 2018-04-15 14:00:29
# Size of source mod 2**32: 220 bytes
from django import forms

class MessageForm(forms.Form):
    message = forms.CharField(label='Message', max_length=1024, widget=forms.TextInput(attrs={'placeholder': 'Type message here'}))