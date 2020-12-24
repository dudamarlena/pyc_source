# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/movister/env/src/django-email-html/email_html/models.py
# Compiled at: 2015-10-13 09:05:53
from django.conf import settings
from django.core import mail
import django
from .mail import send_mail as send_html_mail
mail.send_mail = send_html_mail
if django.VERSION[0] == 1 and django.VERSION[1] >= 7:
    from django.core.exceptions import AppRegistryNotReady
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
    except AppRegistryNotReady:
        from django.contrib.auth.models import User

else:
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
    except ImportError:
        from django.contrib.auth.models import User

def email_user(self, subject, message, from_email=None, **kwargs):
    """
    Sends an email to this User.
    """
    send_html_mail(subject, message, from_email, [self.email], **kwargs)


User.email_user = email_user
if 'mailer' in settings.INSTALLED_APPS:
    import mailer
    mailer.send_mail = send_html_mail