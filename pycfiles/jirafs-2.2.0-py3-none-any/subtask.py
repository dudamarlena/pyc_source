# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/acoddington/Documents/Projects/jirafs/jirafs/commands/subtask.py
# Compiled at: 2019-03-11 23:04:44
from jirafs import utils
from jirafs.plugin import CommandPlugin

class Command(CommandPlugin):
    """Create a subtask of a given issue."""
    MIN_VERSION = '1.15'
    MAX_VERSION = '1.99.99'

    def main(self, folder, args, **kwargs):
        summary = (' ').join(args.summary)
        folder.jira.create_issue(fields={'project': {'key': folder.issue.fields.project.key}, 
           'summary': summary, 
           'issuetype': {'name': 'Sub-task'}, 
           'parent': {'id': folder.issue.key}})
        commands = utils.get_installed_commands()
        jira = utils.lazy_get_jira()
        commands['fetch'].execute_command([], jira=jira, path=folder.path, command_name='fetch')

    def add_arguments(self, parser):
        parser.add_argument('summary', nargs='+')