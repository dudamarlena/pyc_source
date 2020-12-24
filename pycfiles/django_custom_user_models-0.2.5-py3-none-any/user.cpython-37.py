# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: M:\Programming\Project\django-auth\auth\CustomAuth\models\user.py
# Compiled at: 2020-02-24 06:41:37
# Size of source mod 2**32: 232 bytes
from .abstract_user import AbstractUser

class User(AbstractUser):
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'