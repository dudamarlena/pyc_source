# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/project/get_favorites.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from get_project import GetProject

class GetFavorites(GetProject):
    __domain__ = 'project'
    __operation__ = 'get-favorite'
    mode = None

    def __init__(self):
        GetProject.__init__(self)

    def parse_parameters(self, **params):
        GetProject.parse_parameters(self, **params)
        self._number = None
        self._name = None
        self.set_multiple_result_mode()
        self.object_ids = self._ctx.get_favorited_ids_for_kind('Project', refresh=True)
        return