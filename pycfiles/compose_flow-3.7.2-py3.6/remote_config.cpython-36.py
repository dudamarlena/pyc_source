# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/compose_flow/commands/subcommands/remote_config.py
# Compiled at: 2020-05-06 10:05:57
# Size of source mod 2**32: 1770 bytes
"""
Remote configuration subcommand
"""
import os
from .base import BaseSubcommand
from compose_flow import docker
from compose_flow.errors import NoSuchConfig
from compose_flow.utils import render, yaml_load
DEFAULT_CF_REMOTES_CONFIG_NAME = os.environ.get('CF_REMOTES_CONFIG_NAME', 'compose-flow-remotes')

class RemoteConfig(BaseSubcommand):
    __doc__ = '\n    Subcommand for managing remote configuration\n    '

    def __init__(self, *args, **kwargs):
        self.config_name = kwargs.pop('config_name', DEFAULT_CF_REMOTES_CONFIG_NAME)
        (super().__init__)(*args, **kwargs)

    @classmethod
    def fill_subparser(cls, parser, subparser):
        subparser.add_argument('action')

    def cat(self):
        """
        Prints the loaded compose file to stdout
        """
        print(self.load())

    @property
    def data(self):
        try:
            content = self.load()
        except NoSuchConfig:
            content = {}

        if not content:
            return content
        else:
            rendered = render(content)
            return yaml_load(rendered)

    def is_missing_config_okay(self, exc):
        return True

    def is_missing_env_arg_okay(self):
        return True

    def is_missing_profile_okay(self, exc):
        return True

    def load(self) -> str:
        """
        Loads the compose file that is generated from all the items listed in the profile
        """
        config = docker.get_config(self.config_name)
        return config

    def render_buf(self, fh, runtime_config: bool=True):
        try:
            content = self.load()
        except NoSuchConfig:
            content = None

        if not content:
            return
        fh.write(content)