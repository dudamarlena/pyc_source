# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/acoddington/Documents/Projects/jirafs/jirafs/commands/assign.py
# Compiled at: 2020-01-13 00:37:20
# Size of source mod 2**32: 618 bytes
from jirafs.plugin import CommandPlugin

class Command(CommandPlugin):
    __doc__ = 'Assign the current task to a user'
    MIN_VERSION = '2.0.0'
    MAX_VERSION = '3.0.0'

    def main(self, args, folder, **kwargs):
        username = args.username
        if not username:
            username = folder.get_config().get(folder.jira_base, 'username')
        folder.jira.assign_issue(folder.issue, username)
        folder.log('Successfully assigned %s to %s.',
          args=(folder.issue.key, username))

    def add_arguments(self, parser):
        parser.add_argument('username', nargs='?', type=str)