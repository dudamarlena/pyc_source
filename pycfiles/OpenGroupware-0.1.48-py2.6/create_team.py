# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/team/create_team.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from coils.core.logic import CreateCommand
from keymap import COILS_TEAM_KEYMAP
from command import TeamCommand

class CreateTeam(CreateCommand, TeamCommand):
    __domain__ = 'team'
    __operation__ = 'new'

    def prepare(self, ctx, **params):
        self.keymap = COILS_TEAM_KEYMAP
        self.entity = Team
        CreateCommand.prepare(self, ctx, **params)

    def parse_parameters(self, **params):
        CreateCommand.parse_parameters(self, **params)

    def fill_missing_values(self):
        pass

    def run(self):
        if self._ctx.is_admin:
            CreateCommand.run(self)
            self.fill_missing_values()
            self.set_membership()
            self.save()
        else:
            raise CoilsException('Update of a team entity requires administrative privileges')