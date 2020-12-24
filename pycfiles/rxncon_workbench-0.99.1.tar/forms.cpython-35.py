# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mathias/tbp/django_rxncon_site/src/rule_based/forms.py
# Compiled at: 2018-06-27 10:02:27
# Size of source mod 2**32: 335 bytes
from django import forms
from .models import Rule_based_from_rxnconsys

class RuleForm(forms.ModelForm):

    class Meta:
        model = Rule_based_from_rxnconsys
        fields = [
         'comment']


class DeleteRuleForm(forms.ModelForm):

    class Meta:
        model = Rule_based_from_rxnconsys
        fields = []