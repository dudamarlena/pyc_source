# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/update_map.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *
from coils.foundation import Route, Process, Message

class UpdateMap(Command):
    __domain__ = 'map'
    __operation__ = 'set'

    def parse_parameters(self, **params):
        Command.parse_parameters(self, **params)

    def run(self, **params):
        pass