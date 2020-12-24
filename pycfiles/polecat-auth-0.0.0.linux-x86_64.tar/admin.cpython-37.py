# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.7/site-packages/polecat_auth/admin.py
# Compiled at: 2019-07-25 22:51:52
# Size of source mod 2**32: 473 bytes
from polecat.admin.command import Command
from polecat.model.db import Q
from .models import User

class CreateUser(Command):

    def get_params(self):
        return (
         self.Argument(('email', )),
         self.Argument(('password', )),
         self.Option(('--name', )))

    def run(self, email, password, name=None):
        Q(User).insert(email=email,
          password=password,
          name=name).execute()