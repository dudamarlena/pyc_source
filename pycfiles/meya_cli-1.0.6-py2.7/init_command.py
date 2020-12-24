# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/meya_cli/init_command.py
# Compiled at: 2018-09-14 11:23:44
from __future__ import print_function
from __future__ import absolute_import
import os
from meya_cli import MeyaConfig, DownloadCommand
from meya_cli.base_command import BaseCommand
from meya_cli.path_utils import ensure_directory
PREPOPULATED_GITIGNORE = '\nenv/\n__pycache__/\n*.py[cod]\nmeya-config.yaml\n'
MINIMAL_INIT = False

class InitCommand(BaseCommand):
    INVOCATION = 'init'
    DESCRIPTION = 'initialize a Meya bot, if you know your user api key & bot ID. The easiest way to use this command is to copy it from bot studio.'
    ARGUMENTS = [
     (
      'api_key', {'help': 'api key, found in bot studio.'}),
     (
      'bot_id', {'help': 'id of bot, found in bot studio.'}),
     (
      'api_root',
      {'help': 'optional, specify a different URL with which to access the Meya API.', 'nargs': '?'})]

    def perform(self):
        if os.path.isfile('meya-config.yaml'):
            print("Aborting initialization; 'meya-config.yaml' already exists. You can either run 'meya-cli download' to download the most recent bot contents, or remove it and rerun this command.")
            return
        with open('meya-config.yaml', 'w') as (f):
            f.write('api_key: ' + self.args.api_key + '\n')
            f.write('bot_id: ' + self.args.bot_id + '\n')
            if self.args.api_root:
                f.write('api_root: ' + self.args.api_root + '\n')
        if not MINIMAL_INIT:
            print('Ensuring directory structure is created...')
            ensure_directory('flows')
            ensure_directory('cms')
            ensure_directory('components')
        new_config = MeyaConfig('.', self.args.api_key, self.args.bot_id, self.args.api_root)
        DownloadCommand(new_config, []).perform()
        if not MINIMAL_INIT:
            if not os.path.isfile('.gitignore'):
                print("No '.gitignore' file found. Creating one...")
                with open(os.path.join('.gitignore'), 'w') as (f):
                    f.write(PREPOPULATED_GITIGNORE)