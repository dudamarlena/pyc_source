# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.7/site-packages/polecat_auth/models.py
# Compiled at: 2019-07-26 03:33:05
# Size of source mod 2**32: 485 bytes
from polecat import model
from polecat.model import omit
__all__ = ('User', 'JWTType')

class User(model.Model):
    name = model.TextField()
    email = model.EmailField(unique=True, null=False)
    password = model.PasswordField(omit=(omit.ALL))
    created = model.DatetimeField(default=(model.Auto))
    logged_out = model.DatetimeField(omit=(omit.ALL))


class JWTType(model.Type):
    token = model.TextField()
    user = model.RelatedField(User)