# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/acoddington/Documents/Projects/jirafs/jirafs/commands/macropatch.py
# Compiled at: 2019-03-11 23:04:44
# Size of source mod 2**32: 1107 bytes
import io
from jirafs.plugin import CommandPlugin

class Command(CommandPlugin):
    __doc__ = ' Merge remote changes into your local copy '
    RUN_FOR_SUBTASKS = True
    TRY_SUBFOLDERS = True
    MIN_VERSION = '1.15'
    MAX_VERSION = '1.99.99'

    def handle(self, args, folder, **kwargs):
        return self.cmd(folder, args)

    def add_arguments(self, parser):
        parser.add_argument('action',
          default='get',
          choices=[
         'get',
         'reset'])

    def main(self, folder, args):
        path = folder.get_metadata_path('macros_applied.patch')
        if args.action == 'reset':
            with io.open(path, 'w', encoding='utf-8') as (out):
                out.write('\n\n')
            print('Macro patch successfully reset. Be sure to run `jirafs commit` or `jirafs submit` for these changes to take effect.')
        else:
            if args.action == 'get':
                with io.open(path, 'r', encoding='utf-8') as (in_):
                    print(in_.read())