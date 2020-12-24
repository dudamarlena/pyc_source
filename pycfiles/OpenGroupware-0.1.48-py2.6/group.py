# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/horde/apis/group.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from api import HordeAPI

class HordeGroupAPI(HordeAPI):

    def api_group_exists(self, args):
        team = self.context.run_command('team::get', id=args[0])
        if team is None:
            return False
        else:
            return True

    def api_group_getname(self, args):
        team = self.context.run_command('team::get', id=args[0])
        if team is None:
            return
        else:
            return team.name

    def api_group_getdata(self, args):
        """ Return: { id ->  { name, email, users } } """
        result = {}
        team = self.context.run_command('team::get', id=args[0])
        if team is None:
            return
        else:
            return {'name': team.name, 'email': team.email, 
               'users': self.context.run_command('team::get-logins', team=team)}

    def api_group_listall(self, args):
        if len(args):
            account = self.context.run_command('account::get', login=args[0])
            if account is not None:
                teams = self.context.run_command('team::get', member_id=account.object_id)
            else:
                teams = []
        else:
            teams = self.context.run_command('team::list')
        result = {}
        for team in teams:
            result[team.object_id] = team.name

        return result

    def api_group_listusers(self, args):
        team = self.context.run_command('team::get', id=args[0])
        if team is None:
            return []
        else:
            return self.context.run_command('team::get-logins', team=team)
            return

    def api_group_listgroups(self, args):
        account = self.context.run_command('account::get', login=args[0])
        if account is not None:
            teams = self.context.run_command('team::get', member_id=account.object_id)
        else:
            teams = []
        result = {}
        for team in teams:
            result[team.object_id] = team.name

        return result

    def api_group_search(self, args):
        criteria = [{'key': 'name', 'expression': 'ILIKE', 'value': ('%{0}%').format(args[0])}]
        result = {}
        for team in self.context.run_command('team::search', criteria=criteria):
            result[team.object_id] = team.name

        return result