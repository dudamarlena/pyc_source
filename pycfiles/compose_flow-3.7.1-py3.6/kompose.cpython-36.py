# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/compose_flow/commands/subcommands/kompose.py
# Compiled at: 2020-01-28 12:24:29
# Size of source mod 2**32: 1230 bytes
"""
Kompose subcommand
"""
import argparse, logging, os
from .passthrough_base import PassthroughBaseSubcommand
from compose_flow import errors
DEFAULT_COMPOSE_FILENAME = 'docker-compose.yml'

class Kompose(PassthroughBaseSubcommand):
    __doc__ = '\n    Subcommand for migrating to Kubernetes with kompose commands\n    '
    command_name = 'kompose'
    dirty_working_copy_okay = True
    update_version_env_vars = True

    def __init__(self, *args, check_profile=True, version=None, **kwargs):
        self.check_profile = check_profile
        self._version = version
        (super().__init__)(*args, **kwargs)

    def get_command(self):
        command = super().get_command()
        profile = self.workflow.profile
        command.extend(['-f', profile.filename])
        command.extend(['-o', 'compose-flow-kompose.yml'])
        return command

    @property
    def logger(self) -> logging.Logger:
        return logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    @property
    def version(self):
        """
        Returns the version in the environment, unless it was overridden in this Compose instance
        """
        return self._version or self.env.version