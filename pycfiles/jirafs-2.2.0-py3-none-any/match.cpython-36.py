# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/acoddington/Documents/Projects/jirafs/jirafs/commands/match.py
# Compiled at: 2019-03-11 23:04:44
# Size of source mod 2**32: 3950 bytes
import json, os, subprocess
from jirafs.exceptions import JirafsError
from jirafs.plugin import CommandPlugin, CommandResult
from jirafs.utils import run_command_method_with_kwargs

class Command(CommandPlugin):
    __doc__ = ' Check whether a given dotpath matches an expected value '
    TRY_SUBFOLDERS = True
    MIN_VERSION = '1.15'
    MAX_VERSION = '1.99.99'

    def handle(self, args, folder, **kwargs):
        return self.cmd(folder,
          (args.field_name),
          (args.field_value),
          isjson=(args.json),
          negate=(args.negate),
          raw=(args.raw),
          quiet=(args.quiet),
          execute=(args.execute),
          execute_here=(args.execute_here))

    def add_arguments(self, parser):
        parser.add_argument('field_name')
        parser.add_argument('field_value')
        parser.add_argument('--json',
          help='Process the provided field value as JSON',
          action='store_true',
          default=False)
        parser.add_argument('--execute',
          help='Execute a command for each matching result; by default, will be executed from within the matching folder directory when executed on a folder containing multiple ticket folders.  See --execute-here to change this behavior. The string {} will be replaced with the folder directory  path.',
          default=None)
        parser.add_argument('--execute-here',
          help="Do not switch directories to matching folders's paths when using --execute.",
          action='store_true',
          default=False)
        parser.add_argument('--negate',
          help='Compare the field value without applying plugin transformations',
          action='store_true',
          default=False)
        parser.add_argument('--raw',
          help='Return the field value without applying plugin transformations',
          action='store_true',
          default=False)
        parser.add_argument('--quiet',
          help='Print no message to stdout indicating success or failure',
          action='store_true',
          default=False)

    def main(self, folder, field_name, field_value, isjson, negate, raw, quiet, execute, execute_here):
        actual_value = run_command_method_with_kwargs('field',
          method='get_field_value_by_dotpath',
          folder=folder,
          field_name=field_name,
          raw=raw)
        if isjson:
            field_value = json.loads(field_value)
        success = actual_value == field_value
        comparison_result = ' != '
        if success:
            comparison_result = ' == '
        message = '{left} {comparison} {right}'.format(left=actual_value,
          comparison=comparison_result,
          right=field_value)
        if negate:
            success = not success
        if execute:
            if success:
                execute = execute.replace('{}', folder.path)
                subprocess.call(execute,
                  shell=True,
                  cwd=(os.getcwd() if execute_here else folder.path))
        return (
         message if not quiet else None,
         0 if success else 1)

    def cmd(self, *args, **kwargs):
        message, return_code = (self.main)(*args, **kwargs)
        return CommandResult(message, return_code=return_code)