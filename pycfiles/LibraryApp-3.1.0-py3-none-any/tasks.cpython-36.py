# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kevin/Documents/LibraryApp/LibAppDjango/feedback/tasks.py
# Compiled at: 2019-07-29 07:44:06
# Size of source mod 2**32: 832 bytes
from celery.decorators import task
from celery.utils.log import get_task_logger
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from feedback.emails import send_feedback_email
from feedback.emails import send_periodic_email
logger = get_task_logger(__name__)

@task(name='send_feedback_email_task')
def send_feedback_email_task(email, message):
    """sends an email when feedback form is filled successfully"""
    logger.info('Sent feedback email')
    return send_feedback_email(email, message)


@periodic_task(run_every=crontab(minute='*/1'),
  name='sendperiodic_email',
  ignore_result=True)
def send_periodic_email_task():
    logger.info('Sent periodic email')
    send_periodic_email()