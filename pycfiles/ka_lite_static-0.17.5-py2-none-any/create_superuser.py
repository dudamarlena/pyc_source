# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/contrib/auth/create_superuser.py
# Compiled at: 2018-07-11 18:15:30
"""
Create a superuser from the command line. Deprecated; use manage.py
createsuperuser instead.
"""
if __name__ == '__main__':
    from django.core.management import call_command
    call_command('createsuperuser')