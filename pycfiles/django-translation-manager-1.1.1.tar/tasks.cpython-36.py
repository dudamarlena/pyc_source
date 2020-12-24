# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hansek/projects/django-translation-manager/translation_manager/tasks.py
# Compiled at: 2020-01-20 12:29:58
# Size of source mod 2**32: 577 bytes
from django.core.management import call_command
from django.core.cache import cache
from .settings import get_settings
if get_settings('TRANSLATIONS_PROCESSING_METHOD') == 'async_django_rq':
    from django_rq import job

    @job(get_settings('TRANSLATIONS_PROCESSING_QUEUE'))
    def makemessages_task():
        call_command('makemessages')
        cache.delete(get_settings('TRANSLATIONS_PROCESSING_STATE_CACHE_KEY'))


else:

    def makemessages_task():
        call_command('makemessages')
        cache.delete(get_settings('TRANSLATIONS_PROCESSING_STATE_CACHE_KEY'))