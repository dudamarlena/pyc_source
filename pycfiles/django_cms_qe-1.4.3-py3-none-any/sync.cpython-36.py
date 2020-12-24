# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomas/git/euroix/django-cms-qe/cms_qe_newsletter/external_services/sync.py
# Compiled at: 2019-02-04 04:18:45
# Size of source mod 2**32: 2653 bytes
from django.core.exceptions import ObjectDoesNotExist
from requests.exceptions import HTTPError
from . import mailchimp
from ..models import SERVICE_MAILCHIMP, SUBSCRIBE, UNSUBSCRIBE, Subscriber, SubscribeTask
SERVICE_TO_MODULE = {SERVICE_MAILCHIMP: mailchimp}

def sync_mailing_lists():
    """
    Download mailing lists from external services like Mailchimp.
    """
    mailchimp.sync_mailing_lists()


def sync_tasks():
    """
    Processing tasks yielding same tuple as :py:func:`~.sync_task` function.
    """
    tasks = SubscribeTask.objects.all()
    for task in tasks:
        try:
            try:
                result, message = sync_task(task)
            except Exception as exc:
                result, message = False, str(exc)

        finally:
            if result is False:
                task.failure(message)
            yield (
             result, '{}: {}'.format(task, message))


def sync_task(task):
    """
    Processing task returning tuple of status (``True`` for success, ``False`` for
    some failure and ``None`` for warnings) and message.
    """
    if not task.should_process():
        return (None, 'Skipped')
    service = SERVICE_TO_MODULE.get(task.mailing_list.external_service)
    if not service:
        return (
         False, 'Unsupported service {}'.format(task.mailing_list.external_service))
    try:
        if task.type == SUBSCRIBE:
            sync_subscribe(service, task)
        else:
            if task.type == UNSUBSCRIBE:
                sync_unsubscribe(service, task)
    except HTTPError as exc:
        text = exc.response.text
        if 'fake or invalid' in text:
            Subscriber.objects.filter(email=(task.email)).all().delete()
            task.delete()
            return (None, 'Email is invalid or fake and is deleted\n{}'.format(text))
        return (
         False, '{}\n{}'.format(text, exc))
    except ObjectDoesNotExist:
        task.delete()
        return (None, 'Subscriber does not exist anymore, deleting task')
    except Exception as exc:
        return (
         False, str(exc))
    else:
        task.delete()
        return (True, 'OK')


def sync_subscribe(service, task):
    subscriber = Subscriber.objects.get(mailing_list=(task.mailing_list), email=(task.email))
    external_id = service.sync_subscribe(task.mailing_list.external_id, task.email, task.first_name, task.last_name)
    subscriber.external_id = external_id
    subscriber.save()


def sync_unsubscribe(service, task):
    service.sync_unsubscribe(task.mailing_list.external_id, task.email)