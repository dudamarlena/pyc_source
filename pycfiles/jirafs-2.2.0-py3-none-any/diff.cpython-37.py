# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/acoddington/Documents/Projects/jirafs/jirafs/commands/diff.py
# Compiled at: 2020-01-13 00:37:20
# Size of source mod 2**32: 361 bytes
from jirafs.plugin import CommandPlugin

class Command(CommandPlugin):
    __doc__ = ' Print a diff of locally-changed files '
    MIN_VERSION = '2.0.0'
    MAX_VERSION = '3.0.0'

    def main(self, folder, **kwargs):
        result = folder.run_git_command('diff')
        if result:
            result = result.strip()
        print(result)
        return result