# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Ozgur/Sites/senpilic.com.tr/senpilic/contact/nospam/fields.py
# Compiled at: 2012-10-04 06:34:40
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from widgets import HoneypotWidget

class HoneypotField(forms.BooleanField):

    def __init__(self, *args, **kwargs):
        super(HoneypotField, self).__init__(widget=HoneypotWidget, required=False, error_messages={'checked': _("Please don't check this box.")}, *args, **kwargs)

    def clean(self, value):
        val = super(HoneypotField, self).clean(value)
        if val:
            raise ValidationError(self.error_messages['checked'])
        return val