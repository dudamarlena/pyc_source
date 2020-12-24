# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/review_together/forms.py
# Compiled at: 2015-02-01 18:20:05
from django import forms
from django.utils.translation import ugettext_lazy as _
from djblets.extensions.forms import SettingsForm

class ReviewTogetherSettingsForm(SettingsForm):
    hub_url = forms.CharField(label=_('TogetherJS Hub URL'), required=False)