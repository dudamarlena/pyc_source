# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/acoddington/Documents/Projects/jirafs/jirafs/commands/field.py
# Compiled at: 2020-01-13 00:37:20
# Size of source mod 2**32: 1721 bytes
import json
from jirafs.exceptions import JirafsError
from jirafs.plugin import CommandPlugin, CommandResult

class Command(CommandPlugin):
    __doc__ = ' Get the status of the current ticketfolder '
    TRY_SUBFOLDERS = True
    MIN_VERSION = '2.0.0'
    MAX_VERSION = '3.0.0'

    def handle(self, args, folder, **kwargs):
        return self.cmd(folder, (args.field_name), raw=(args.raw), formatted=(args.formatted))

    def add_arguments(self, parser):
        parser.add_argument('--raw',
          help='Return the field value without applying plugin transformations',
          action='store_true',
          default=False)
        parser.add_argument('--formatted',
          help='Format JSON output with indentation and sorted keys.',
          action='store_true',
          default=False)
        parser.add_argument('field_name')

    def main(self, folder, field_name, raw=False, formatted=False):
        special_fields = {'new_comment':folder.get_new_comment, 
         'links':folder.get_links, 
         'fields':folder.get_fields}
        if field_name in special_fields:
            data = special_fields[field_name]()
        else:
            data = folder.get_field_value_by_dotpath(field_name, raw)
        if isinstance(data, (list, dict)):
            kwargs = {}
            if formatted:
                kwargs = {'indent':4,  'sort_keys':True}
            data = (json.dumps)(data, **kwargs)
        return data

    def cmd(self, *args, **kwargs):
        data = (self.main)(*args, **kwargs)
        return CommandResult(data, no_format=True)