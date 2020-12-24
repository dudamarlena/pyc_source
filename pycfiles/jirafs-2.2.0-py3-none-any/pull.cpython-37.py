# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/acoddington/Documents/Projects/jirafs/jirafs/commands/pull.py
# Compiled at: 2020-01-13 00:37:20
# Size of source mod 2**32: 516 bytes
from jirafs.plugin import CommandPlugin
from jirafs.utils import run_command_method_with_kwargs

class Command(CommandPlugin):
    __doc__ = ' Fetch and merge remote changes '
    RUN_FOR_SUBTASKS = True
    TRY_SUBFOLDERS = True
    MIN_VERSION = '2.0.0'
    MAX_VERSION = '3.0.0'

    def main(self, folder, **kwargs):
        fetch_result = run_command_method_with_kwargs('fetch', folder=folder)
        merge_result = run_command_method_with_kwargs('merge', folder=folder)
        return (
         fetch_result, merge_result)