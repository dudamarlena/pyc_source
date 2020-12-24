# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dzhiltsov/Development/vcslib/vcs/commands/standup.py
# Compiled at: 2015-05-15 06:06:58
from vcs.commands.log import LogCommand

class StandupCommand(LogCommand):

    def handle_repo(self, repo, **options):
        options['all'] = True
        options['start_date'] = '1day'
        username = repo.get_user_name()
        options['author'] = username + '*'
        return super(StandupCommand, self).handle_repo(repo, **options)