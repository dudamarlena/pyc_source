# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/account/create_account.py
# Compiled at: 2012-10-12 07:02:39
from datetime import datetime, timedelta
from pytz import timezone
from sqlalchemy import *
from sqlalchemy.orm import *
from coils.founcation import *
from coils.core import *
from keymap import COILS_ACCOUNT_KEYMAP

class CreateAccount(Command):
    __domain__ = 'account'
    __operation__ = 'new'

    def __init__(self):
        Command.__init__(self)

    def parse_parameters(self, **params):
        Command.parse_parameters(self, **params)

    def run(self):
        raise NotImplementedException('account::new not implemented')