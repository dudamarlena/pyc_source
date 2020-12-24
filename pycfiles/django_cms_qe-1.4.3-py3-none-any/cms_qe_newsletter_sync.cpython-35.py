# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomas/git/euroix/django-cms-qe/cms_qe_newsletter/management/commands/cms_qe_newsletter_sync.py
# Compiled at: 2019-02-04 04:18:45
# Size of source mod 2**32: 807 bytes
from django.core.management.base import BaseCommand
from cms_qe_newsletter import logger
from cms_qe_newsletter.external_services.sync import sync_tasks

class Command(BaseCommand):
    __doc__ = '\n    Command processes the queue to subscribing and unsubscribing\n    on the external services. Usage of command with ``manage.py``::\n\n        python -m manage.py cms_qe_newsletter_sync\n    '

    def handle(self, *args, **options):
        logger.info('Newsletter sync started...')
        for task_result, task_message in sync_tasks():
            if task_result is None:
                logger.warning(task_message)
            else:
                if task_result is False:
                    logger.error(task_message)
                else:
                    logger.info(task_message)

        logger.info('Newsletter sync finished...')