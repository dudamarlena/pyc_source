# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/bin/daily_cleanup.py
# Compiled at: 2018-07-11 18:15:30
"""
Daily cleanup job.

Can be run as a cronjob to clean out old data from the database (only expired
sessions at the moment).
"""
import warnings
from django.core import management
if __name__ == '__main__':
    warnings.warn('The `daily_cleanup` script has been deprecated in favor of `django-admin.py clearsessions`.', PendingDeprecationWarning)
    management.call_command('clearsessions')