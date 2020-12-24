# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/strip/.local/share/virtualenvs/django-pursed/lib/python3.5/site-packages/wallet/errors.py
# Compiled at: 2017-04-18 11:29:16
# Size of source mod 2**32: 315 bytes
from django.db import IntegrityError

class InsufficientBalance(IntegrityError):
    __doc__ = "Raised when a wallet has insufficient balance to\n    run an operation.\n\n    We're subclassing from :mod:`django.db.IntegrityError`\n    so that it is automatically rolled-back during django's\n    transaction lifecycle.\n    "