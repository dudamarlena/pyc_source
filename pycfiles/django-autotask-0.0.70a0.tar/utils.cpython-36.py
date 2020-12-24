# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-autotask/djautotask/utils.py
# Compiled at: 2020-01-31 13:20:27
# Size of source mod 2**32: 460 bytes
from django.conf import settings

class DjautotaskSettings:

    def get_settings(self):
        request_settings = {'timeout':30.0, 
         'batch_size':50, 
         'max_attempts':3, 
         'keep_completed_hours':8, 
         'batch_query_size':400}
        if hasattr(settings, 'DJAUTOTASK_CONF_CALLABLE'):
            request_settings.update(settings.DJAUTOTASK_CONF_CALLABLE())
        return request_settings