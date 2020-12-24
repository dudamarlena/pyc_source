# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/meya_cli/base_command.py
# Compiled at: 2018-09-14 11:23:44
from __future__ import print_function
from __future__ import absolute_import
import argparse, os
from meya_cli.path_utils import has_hidden_component

class BaseCommand(object):
    INVOCATION = None
    DESCRIPTION = ''
    ARGUMENTS = []

    def __init__(self, config, argv):
        self.config = config
        self.args = type(self).arg_parser().parse_args(argv)

    @property
    def command_string(self):
        """
        Override INVOCATION in sub-class.
        Used for referencing the command as a string in other contexts
        like analytics tools.
        Ex: "init" for InitCommand class
        """
        if self.INVOCATION:
            return self.INVOCATION
        return self.__class__.__name__

    @property
    def api(self):
        from meya_cli.meya_api import MeyaAPI
        return MeyaAPI(self.config.api_key, base_url=self.config.api_root, command_string=self.command_string)

    @classmethod
    def arg_parser(cls):
        parser = argparse.ArgumentParser(prog='meya-cli ' + cls.INVOCATION, description=cls.DESCRIPTION, add_help=False)
        for name, arg_spec in cls.ARGUMENTS:
            parser.add_argument(name, **arg_spec)

        return parser

    def perform(self):
        pass

    @property
    def file_api_root(self):
        return 'files/' + self.config.bot_id + '/'

    def local_files(self):
        paths = []
        for dir, _child_dirs, files in os.walk(self.config.root_dir):
            for file in files:
                path = os.path.join(dir, file)
                if self.config.ignore_dot_files and has_hidden_component(path):
                    continue
                if not self.config.path_matches_autosync_patterns(path):
                    continue
                paths.append(os.path.relpath(path))

        return paths

    def remote_files(self):
        paths = []
        for result in self.api.get(self.file_api_root)['results']:
            abs_path = os.path.join(self.config.root_dir, result['path'])
            paths.append(os.path.relpath(abs_path))

        return paths