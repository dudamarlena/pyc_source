# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/maluki/blog/django_blog/blog_project/contact/tasks.py
# Compiled at: 2019-07-30 05:26:05
# Size of source mod 2**32: 526 bytes
from celery.decorators import task
from celery.utils.log import get_task_logger
from contact.emails import send_contact_email
logger = get_task_logger(__name__)

@task(name='send_contact_email_task')
def send_contact_email_task(email, message):
    """sends an email when contact form is filled successfully"""
    logger.info('Sent contact email')
    return send_contact_email(email, message)