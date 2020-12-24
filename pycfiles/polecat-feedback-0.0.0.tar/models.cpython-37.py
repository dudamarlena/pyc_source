# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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