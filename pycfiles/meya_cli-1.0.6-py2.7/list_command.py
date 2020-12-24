# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/meya_cli/list_command.py
# Compiled at: 2018-09-14 11:23:44
from __future__ import print_function
from __future__ import absolute_import
import os
from meya_cli.base_command import BaseCommand
from meya_cli.path_utils import has_hidden_component

class ListCommand(BaseCommand):
    INVOCATION = 'list'
    DESCRIPTION = "List remote files. By default, these files are downloaded with 'meya-cli download' or uploaded from local copies with 'meya-cli upload'."
    ARGUMENTS = [
     (
      '--local-diff',
      {'help': 'list files only present locally.', 'action': 'store_true'}),
     (
      '--remote-diff',
      {'help': 'list files only present on remote server.', 'action': 'store_true'})]

    def perform(self):
        if self.args.local_diff:
            remote_files = self.remote_files()
            for path in self.local_files():
                if path not in remote_files:
                    print(path)

        elif self.args.remote_diff:
            for path in self.remote_files():
                if not os.path.isfile(path):
                    print(path)

        else:
            for path in self.remote_files():
                print(path)