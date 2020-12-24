# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/enterprise/get_favorite.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from get_enterprise import GetEnterprise

class GetFavorites(GetEnterprise):
    __domain__ = 'enterprise'
    __operation__ = 'get-favorite'
    mode = None

    def __init__(self):
        GetEnterprise.__init__(self)

    def parse_parameters(self, **params):
        Command.parse_parameters(self, **params)
        self._email = None
        self._archived = False
        self.set_multiple_result_mode()
        self.object_ids = self._ctx.get_favorited_ids_for_kind('Enterprise', refresh=True)
        return