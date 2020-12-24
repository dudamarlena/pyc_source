# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/leotrubach/development/django-saas-email/venv/lib/python3.7/site-packages/django_saas_email/tasks.py
# Compiled at: 2019-02-14 13:03:37
# Size of source mod 2**32: 1075 bytes
from django.conf import settings
import django.apps as apps
from .models import Mail
task_queue = getattr(settings, 'DJANGO_SAAS_EMAIL_TASK_QUEUE', 'celery')
decorator_kwargs = getattr(settings, 'DJANGO_SAAS_EMAIL_DECORATOR_KWARGS', {})
if task_queue == 'celery':
    from celery import shared_task as task_decorator
else:
    if task_queue == 'rq':
        from django_rq import job as task_decorator
    else:
        raise RuntimeError('Only `celery` and `rq` task queues are supported.')

@task_decorator(**decorator_kwargs)
def send_asynchronous_mail(mail_uuid, sendgrid_api=False):
    """Send an asynchronous mail by the given ID."""
    try:
        app_model_name = settings.DJANGO_SAAS_EMAIL_MAIL_MODEL
    except AttributeError:
        mail_model = Mail
    else:
        app_label, model_name = app_model_name.split('.')
        mail_model = apps.get_model(app_label, model_name)
    try:
        mail = mail_model.objects.get(id=mail_uuid)
    except Mail.DoesNotExist:
        raise AttributeError('There is no mail with that UUID')

    mail.send(sendgrid_api=sendgrid_api)