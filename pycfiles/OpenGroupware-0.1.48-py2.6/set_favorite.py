# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/project/set_favorite.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from coils.logic.address import GetCompany
from command import ProjectCommand

class SetFavorite(Command, ProjectCommand):
    __domain__ = 'project'
    __operation__ = 'set-favorite'
    mode = None

    def __init__(self):
        Command.__init__(self)

    def parse_parameters(self, **params):
        if 'ids' in params:
            self.object_ids = [ int(x) for x in params.get('ids') ]
        elif 'objects' in params:
            self.object_ids = [ int(x.object_id) for x in params.get('objects') ]
        else:
            raise CoilsException('No ids or objects parameter provided to project::set-favorite')

    def run(self):
        self._ctx.set_favorited_ids_for_kind('project', self.object_ids)