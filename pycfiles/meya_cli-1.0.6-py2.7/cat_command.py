# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/meya_cli/cat_command.py
# Compiled at: 2018-09-14 11:23:44
from __future__ import print_function
from __future__ import absolute_import
import os
from meya_cli.base_command import BaseCommand

class CatCommand(BaseCommand):
    INVOCATION = 'cat'
    DESCRIPTION = 'Show the contents of remote files.'
    ARGUMENTS = [
     (
      'files', {'nargs': '+', 'help': 'files to show on standard output.'})]

    def perform(self):
        for file in self.args.files:
            abs_path = os.path.abspath(file)
            meya_path = os.path.relpath(abs_path, start=self.config.root_dir)
            result = self.api.get(self.file_api_root + meya_path)
            print(result['contents'])