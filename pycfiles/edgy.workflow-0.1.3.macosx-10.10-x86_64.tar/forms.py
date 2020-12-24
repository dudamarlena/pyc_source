# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rd/Work/Edgy/workflow/.virtualenv-python/lib/python2.7/site-packages/edgy/workflow/ext/django_workflow/forms.py
# Compiled at: 2016-02-21 07:40:32
from __future__ import absolute_import, print_function, unicode_literals
from django import forms

class TransitionForm(forms.models.ModelForm):

    def __init__(self, *args, **kwargs):
        self.transition = kwargs.pop(b'transition')
        super(TransitionForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        transition_handler = getattr(self.instance, self.transition)
        try:
            transition_handler()
            return super(TransitionForm, self).save(commit=commit)
        except Exception as e:
            raise