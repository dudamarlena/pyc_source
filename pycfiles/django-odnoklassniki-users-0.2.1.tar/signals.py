# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture_old/env/src/django-odnoklassniki-users/odnoklassniki_users/signals.py
# Compiled at: 2015-03-21 09:08:30
from django.dispatch import receiver
from django.conf import settings
from django.dispatch.dispatcher import Signal
from .tasks import OdnoklassnikiUsersFetchUsers
users_to_fetch = Signal(providing_args=['ids'])

@receiver(users_to_fetch)
def fetch_users(ids, **kwargs):
    only_expired = getattr(settings, 'ODNOKLASSNIKI_USERS_FETCH_ONLY_EXPIRED_USERS', True)
    async = getattr(settings, 'ODNOKLASSNIKI_USERS_FETCH_USERS_ASYNC', False)
    params = dict(ids=ids, only_expired=only_expired)
    if async:
        OdnoklassnikiUsersFetchUsers.apply_async(kwargs=params)
    else:
        OdnoklassnikiUsersFetchUsers.apply(kwargs=params)