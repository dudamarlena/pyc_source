# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/meya_cli/delete_command.py
# Compiled at: 2018-09-14 11:23:44
from __future__ import print_function
from __future__ import absolute_import
import os
from meya_cli.base_command import BaseCommand
from meya_cli.meya_api import MeyaNoSuchFileException

class DeleteCommand(BaseCommand):
    INVOCATION = 'delete'
    DESCRIPTION = 'Delete Meya bot source from a Meya-managed folder. Deletes given bot files on Meya (but not locally)'
    ARGUMENTS = [
     (
      '--remote-diff',
      {'help': 'delete files only found in remote bot.', 'action': 'store_true'}),
     (
      '--local-diff',
      {'help': 'delete files only found in local bot. WARNING: Deletes local files', 'action': 'store_true'}),
     (
      'files',
      {'help': 'file to delete in Meya bot source (local copy preserved)', 'nargs': '*'})]

    def delete(self, path):
        meya_path = os.path.relpath(path, start=self.config.root_dir)
        rel_path = os.path.relpath(path)
        print('Deleting remote ' + rel_path)
        try:
            self.api.delete(self.file_api_root + meya_path)
        except MeyaNoSuchFileException:
            print('No remote file matching ' + meya_path + '; skipping.')

    def perform(self):
        if self.args.files and self.args.remote_diff:
            raise Exception("Cannot specify both 'remote_diff' and a list of files.")
        if self.args.files and self.args.local_diff:
            raise Exception("Cannot specify both 'local_diff' and a list of files.")
        if self.args.remote_diff:
            files = []
            for file in self.remote_files():
                if not os.path.isfile(file):
                    files.append(file)

            if not files:
                print('No remote-only files to be deleted.')
        else:
            if self.args.local_diff:
                files = []
                remote_files = self.remote_files()
                for path in self.local_files():
                    if path not in remote_files:
                        files.append(path)

                if not files:
                    print('No local-only files to be deleted.')
                for file in files:
                    print('Deleting local ' + file)
                    os.unlink(file)

                return
            files = self.args.files
            if not files:
                print('No files specified for deletion.')
            for file in files:
                path = os.path.abspath(file)
                self.delete(path)