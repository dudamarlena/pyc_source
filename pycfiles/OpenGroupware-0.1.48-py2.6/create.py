# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/token/create.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from coils.core.logic import CreateCommand
from keymap import COILS_TOKEN_KEYMAP
from command import TokenCommand

class CreateToken(CreateCommand, TokenCommand):
    __domain__ = 'token'
    __operation__ = 'new'

    def prepare(self, ctx, **params):
        self.keymap = COILS_TOKEN_KEYMAP
        self.entity = AuthenticationToken
        CreateCommand.prepare(self, ctx, **params)

    def parse_parameters(self, **params):
        CreateCommand.parse_parameters(self, **params)

    def run(self):
        CreateCommand.run(self)
        self.obj.account_id = self._ctx.account_id
        self.save()