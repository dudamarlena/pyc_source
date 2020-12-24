# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/sentry_mailagain/forms.py
# Compiled at: 2013-08-30 09:52:34
from django.forms import forms
from sentry.web.forms.fields import RangeField

class MailAgainConfForm(forms.Form):
    mail_again_age = RangeField(help_text='Send a new mail notification if an unresolved event is seen again and the last notification was older than this amount of time', required=False, min_value=0, max_value=168, step_value=1)