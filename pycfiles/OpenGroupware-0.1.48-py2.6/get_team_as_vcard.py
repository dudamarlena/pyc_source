# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/team/get_team_as_vcard.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *
from coils.core.logic import GetCommand
from coils.core.vcard import Render
from get_team import GetTeam

class GetTeamAsVCard(GetTeam):
    __domain__ = 'team'
    __operation__ = 'get-as-vcard'
    mode = None

    def parse_parameters(self, **params):
        if 'object' in params:
            self._object = params.get('object')
        else:
            GetTeam.parse_parameters(self, **params)

    def run(self):
        if hasattr(self, '_object'):
            self._result = Render.render(self._object, self._ctx)
        else:
            GetTeam.run(self)
            if self._result is None:
                return
            if isinstance(self._result, list):
                teams = self._result
                self._result = []
                for team in teams:
                    self._result.append(Render.render(team, self._ctx))

            else:
                self._result = Render.render(self._result, self._ctx)
        return