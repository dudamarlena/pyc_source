# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/meya_cli/download_command.py
# Compiled at: 2018-09-14 11:23:44
from __future__ import print_function
from __future__ import absolute_import
import os
from meya_cli.base_command import BaseCommand
from meya_cli.path_utils import ensure_directory

class DownloadCommand(BaseCommand):
    INVOCATION = 'download'
    DESCRIPTION = 'Download most recent Meya bot source to a Meya-managed folder. Downloads bot files if specified, or the entire bot source otherwise.'
    ARGUMENTS = [
     (
      '--remote-diff',
      {'help': 'download files only found in remote bot.', 'action': 'store_true'}),
     (
      'files', {'nargs': '*', 'help': 'files to download. Currently, bot folders cannot be selectively downloaded. Providing no arguments downloads the entire bot'})]

    def remote_files(self):
        paths = []
        for result in self.api.get(self.file_api_root)['results']:
            abs_path = os.path.join(self.config.root_dir, result['path'])
            paths.append(os.path.relpath(abs_path))

        return paths

    def _write_file(self, write_path, contents):
        if os.path.isfile(write_path):
            print('Downloading ' + os.path.relpath(write_path) + ' (overwrite)')
        else:
            ensure_directory(os.path.dirname(write_path))
            print('Downloading ' + os.path.relpath(write_path))
        with open(write_path, 'w') as (f):
            f.write(contents.encode('utf-8'))

    def _download_files(self, files):
        for file in files:
            write_path = os.path.abspath(file)
            meya_path = os.path.relpath(write_path, start=self.config.root_dir)
            result = self.api.get(self.file_api_root + meya_path)
            self._write_file(write_path, result['contents'])

    def perform(self):
        if self.args.files and self.args.remote_diff:
            raise Exception("Cannot specify both 'remote_diff' and a list of files.")
        if self.args.remote_diff:
            files = []
            for file in self.remote_files():
                if not os.path.isfile(file):
                    files.append(file)

            if not files:
                print('No remote-only files exist.')
            self._download_files(files)
        elif self.args.files:
            self._download_files(self.args.files)
        else:
            files = []
            for result in self.api.get(self.file_api_root)['results']:
                files.append(os.path.join(self.config.root_dir, result['path']))

            self._download_files(files)