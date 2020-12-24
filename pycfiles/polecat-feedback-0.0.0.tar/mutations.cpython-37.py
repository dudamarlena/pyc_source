# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib/python3.7/site-packages/polecat_auth/mutations.py
# Compiled at: 2019-07-27 19:41:46
# Size of source mod 2**32: 943 bytes
from polecat import model
from polecat.auth import jwt
from polecat.model.db import Q
from .exceptions import AuthError
from .models import JWTType, User
__all__ = ('AuthenticateInput', 'Authenticate')

class AuthenticateInput(model.Type):
    email = model.EmailField()
    password = model.PasswordField()

    class Meta:
        input = True


class Authenticate(model.Mutation):
    input = AuthenticateInput
    returns = JWTType

    def resolve(self, email, password):
        result = Q(User).filter(email=email,
          password=password)
        if self.selector:
            if 'user' in self.selector.lookups:
                result = result.select(self.selector.lookups.get('user'))
        result = result.get()
        if not result:
            raise AuthError('Invalid email/password')
        return {'token':jwt({'user_id':result['id'],  'role':'user'}), 
         'user':result}