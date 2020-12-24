# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/recurring_payments/fields.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 673 bytes
from django import forms
from tendenci.apps.recurring_payments.widgets import BillingCycleWidget

class BillingCycleField(forms.MultiValueField):

    def __init__(self, required=True, widget=BillingCycleWidget(attrs=None), label=None, initial=None, help_text=None):
        myfields = ()
        super(BillingCycleField, self).__init__(myfields, required=required, widget=widget, label=label,
          initial=initial,
          help_text=help_text)

    def clean(self, value):
        return self.compress(value)

    def compress(self, data_list):
        if data_list:
            return ','.join(data_list)