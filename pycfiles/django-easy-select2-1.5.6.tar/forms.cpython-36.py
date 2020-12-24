# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/asyncee/git/django-easy-select2/easy_select2/forms.py
# Compiled at: 2018-03-18 12:12:47
# Size of source mod 2**32: 769 bytes
from django import forms
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
M = _('Hold down "Control", or "Command" on a Mac, to select more than one.')

class FixedModelForm(forms.ModelForm):
    __doc__ = '\n    Simple child of ModelForm that removes the \'Hold down "Control" ...\'\n    message that is enforced in select multiple fields.\n\n    See https://github.com/asyncee/django-easy-select2/issues/2\n    and https://code.djangoproject.com/ticket/9321\n    '

    def __init__(self, *args, **kwargs):
        (super(FixedModelForm, self).__init__)(*args, **kwargs)
        msg = force_text(M)
        for name, field in self.fields.items():
            field.help_text = field.help_text.replace(msg, '')