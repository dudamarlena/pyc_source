# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/wojciech/.pyenv/versions/3.7.3/lib/python3.7/site-packages/django_password_validators/password_history/hashers.py
# Compiled at: 2016-02-29 15:25:21
# Size of source mod 2**32: 838 bytes
from django.contrib.auth.hashers import PBKDF2PasswordHasher

class HistoryHasher(PBKDF2PasswordHasher):
    __doc__ = '\n    We need to keep the old password so that when you update django \n    (or configuration change) hashes have not changed. \n    Therefore, special hasher.\n\n    '
    iterations = 200000


class HistoryVeryStrongHasher(PBKDF2PasswordHasher):
    __doc__ = '\n    We need to keep the old password so that when you update django \n    (or configuration change) hashes have not changed. \n    Therefore, special hasher.\n\n    '
    iterations = 2020000