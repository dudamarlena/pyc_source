# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/compose_flow/commands/subcommands/task.py
# Compiled at: 2020-01-28 12:24:29
# Size of source mod 2**32: 2608 bytes
"""
Task subcommand
"""
from functools import lru_cache
import logging, shlex
from .base import BaseSubcommand
from compose_flow.config import get_config
from compose_flow.errors import CommandError
ALLOWED_COMMANDS = [
 'compose-flow', 'rancher']
PROFILE_SUBCOMMANDS = ['compose-flow', 'compose']

class Task(BaseSubcommand):
    update_version_env_vars = True

    @classmethod
    def fill_subparser(self, parser, subparser):
        subparser.add_argument('name', help='the task name to process')

    @property
    def task_name(self):
        return self.workflow.args.name

    @property
    @lru_cache()
    def task_config(self):
        config = get_config(self.workflow)
        try:
            task = config['tasks'][self.task_name]
        except KeyError:
            raise CommandError(f"task name={self.task_name} not found")

        return task

    @property
    def command_split(self):
        command = self.task_config['command']
        return shlex.split(command)

    @property
    def setup_profile(self):
        if self.command_split[1] in PROFILE_SUBCOMMANDS:
            return True
        else:
            return False

    def handle(self):
        if self.command_split[0] not in ALLOWED_COMMANDS:
            raise NotImplementedError('tasks that are not compose-flow are not yet supported')
        subcommand_name = self.command_split[1]
        subcommand = self.get_subcommand(subcommand_name)
        subcommand_args = self.command_split[2:]
        remainder = self.workflow.args_remainder
        if remainder:
            subcommand_args.extend(remainder)
        subcommand.handle(subcommand_args)

    def is_dirty_working_copy_okay(self, exc):
        dirty_working_copy_okay = super().is_dirty_working_copy_okay(exc)
        if not dirty_working_copy_okay:
            if self.workflow.environment_name in ('local', ):
                self.logger.warning('\n\nWARNING: the local environment does not allow a dirty working copy by default.\nin your compose-flow.yml set `options -> local -> dirty_working_copy_okay` to true\n\n')
        return dirty_working_copy_okay

    @property
    def logger(self):
        return logging.getLogger(f"{__name__}.{self.__class__.__name__}")