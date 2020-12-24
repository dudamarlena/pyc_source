# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ahernp/code/django-ahernp/ahernp/dmcm/edit/forms.py
# Compiled at: 2015-11-28 13:36:53
from __future__ import absolute_import
from django import forms
from django.forms.utils import ErrorList
from ..models import Page

class TextErrorList(ErrorList):
    """Format list of errors as text with breaks"""

    def as_textlist(self):
        if not self:
            return ''
        return '%s' % ('<br>').join([ '%s' % e for e in self ])


class BaseModelForm(forms.ModelForm):
    """Base ModelForm using TextErrorList"""

    def __init__(self, *args, **kwargs):
        super(BaseModelForm, self).__init__(*args, **kwargs)
        self.error_class = TextErrorList


class PageForm(BaseModelForm):
    """Form for Page Model"""

    class Meta:
        model = Page
        fields = '__all__'