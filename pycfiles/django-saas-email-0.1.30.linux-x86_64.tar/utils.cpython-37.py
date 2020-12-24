# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/leotrubach/development/django-saas-email/venv/lib/python3.7/site-packages/django_saas_email/utils.py
# Compiled at: 2019-04-11 15:57:24
# Size of source mod 2**32: 572 bytes
from django.conf import settings

def create_and_send_mail(**kwargs):
    from .models import Mail
    from .tasks import send_asynchronous_mail
    mail = (Mail.objects.create_mail)(**kwargs)
    send_asynchronous_mail.delay((mail.id), sendgrid_api=(getattr(settings, 'SENDGRID_API_KEY', False)))


def _noautoescape(template):
    return '{}{}{}'.format('{% autoescape off %}', template, '{% endautoescape %}')