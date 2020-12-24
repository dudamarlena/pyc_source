# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/iwoca/django-seven/django_seven/compat/db/transaction.py
# Compiled at: 2016-07-26 15:41:40
from functools import wraps
import django
from django.db import transaction
if django.VERSION < (1, 6):
    atomic_compat_transaction = transaction.commit_on_success
else:
    atomic_compat_transaction = transaction.atomic
if django.VERSION < (1, 6):

    def managed_transaction(func):
        """ This decorator wraps a function so that all sql executions in the function are atomic

            It's used instead of django.db.transaction.commit_on_success in cases where reporting exceptions is necessary
            as commit_on_success swallows exceptions
        """

        @wraps(func)
        @transaction.commit_manually
        def _inner(*args, **kwargs):
            try:
                ret = func(*args, **kwargs)
            except Exception:
                transaction.rollback()
                raise
            else:
                transaction.commit()
                return ret

        return _inner


else:
    managed_transaction = transaction.atomic