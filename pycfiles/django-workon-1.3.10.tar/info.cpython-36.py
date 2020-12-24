# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/workon/forms/info.py
# Compiled at: 2018-08-30 07:17:09
# Size of source mod 2**32: 859 bytes
from django import forms
from django.db.models import CharField

class InfoField(forms.CharField):

    def __init__(self, *args, **kwargs):
        if 'widget' not in kwargs:
            kwargs['widget'] = InfoInput(text=(kwargs.pop('text', '')))
        (super(InfoField, self).__init__)(*args, **kwargs)


class InfoInput(forms.widgets.HiddenInput):

    def __init__(self, *args, **kwargs):
        self.text = kwargs.pop('text', '')
        (super(InfoInput, self).__init__)(*args, **kwargs)

    def render(self, name, value, attrs={}, **kwargs):
        if 'id' not in attrs:
            attrs['id'] = 'id_%s' % name
        return '<div id="%(id)s" >%(value)s</div>\n                ' % {'id':attrs['id'], 
         'value':value, 
         'text':self.text}