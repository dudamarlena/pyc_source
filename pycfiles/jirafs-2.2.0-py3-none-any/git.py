# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/acoddington/Documents/Projects/jirafs/jirafs/commands/git.py
# Compiled at: 2019-03-11 23:04:44
import pydoc
from jirafs.plugin import CommandPlugin

class Command(CommandPlugin):
    """ Run a git command against this ticketfolder's underlying GIT repo """
    MIN_VERSION = '1.15'
    MAX_VERSION = '1.99.99'

    def handle(self, args, folder, **kwargs):
        return self.cmd(folder, *self.git_arguments)

    def parse_arguments(self, parser, extra_args):
        args, git_arguments = parser.parse_known_args(extra_args)
        self.git_arguments = git_arguments
        return args

    def main(self, folder, *git_arguments):
        result = folder.run_git_command(*git_arguments)
        pydoc.pager(result)
        return result