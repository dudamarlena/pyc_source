# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/compose_flow/commands/subcommands/base.py
# Compiled at: 2020-05-06 10:05:57
# Size of source mod 2**32: 5042 bytes
from functools import lru_cache
import logging
from abc import ABC
from compose_flow import errors, shell
from compose_flow.config import get_config
from compose_flow.errors import CommandError, EnvError, NoSuchConfig, NoSuchProfile, NotConnected, ProfileError, TagVersionError

class BaseSubcommand(ABC):
    __doc__ = '\n    Parent class for any subcommand class\n    '
    dirty_working_copy_okay = False
    profile_checks = [
     'check_env']
    remote_action = True
    rw_env = False
    setup_environment = True
    setup_profile = True
    update_version_env_vars = False

    def __init__(self, workflow):
        self.workflow = workflow

    @property
    def logger(self):
        return logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    def do_validate_profile(self):
        return True

    def execute(self, command: str, **kwargs):
        """
        Executes the given command
        """
        env = kwargs.pop('_env', None) or self.workflow.environment.data
        return (shell.execute)(command, env, **kwargs)

    def get_subcommand(self, name: str) -> object:
        """
        Returns the requested subcommand class by name
        """
        from . import get_subcommand_class
        subcommand_cls = get_subcommand_class(name)
        return subcommand_cls(self.workflow)

    @classmethod
    def fill_subparser(cls, parser, subparser):
        """
        Stub for adding arguments to this subcommand's subparser
        """
        pass

    def handle(self):
        return self.handle_action()

    def handle_action(self):
        action = self.workflow.args.action
        action_fn = getattr(self, f"action_{action}", None)
        if not action_fn:
            action_fn = getattr(self, action, None)
        if action_fn:
            return action_fn()
        self.print_subcommand_help((self.__doc__), error=f"unknown action={action}")

    def is_dirty_working_copy_okay(self, exc: Exception) -> bool:
        """
        Checks to see if the project's compose-flow.yml allows for the env to use a dirty working copy

        To configure an environment to allow a dirty working copy, add the following to the compose-flow.yml

        ```
        options:
          env_name:
            dirty_working_copy_okay: true
        ```

        This defaults to False
        """
        config = get_config(self.workflow) or {}
        env = self.workflow.environment_name
        dirty_working_copy_okay = self.workflow.args.dirty or config.get('options', {}).get(env, {}).get('dirty_working_copy_okay', self.dirty_working_copy_okay)
        return dirty_working_copy_okay

    def is_env_error_okay(self, exc):
        return False

    def is_env_runtime_error_okay(self):
        return False

    def is_missing_config_okay(self, exc):
        return False

    def is_missing_env_arg_okay(self):
        return False

    def is_missing_profile_okay(self, exc):
        return False

    def is_not_connected_okay(self, exc):
        return False

    def is_write_profile_error_okay(self, exc):
        return False

    def print_subcommand_help(self, doc, error=None):
        print(doc.lstrip())
        self.workflow.parser.print_help()
        if error:
            return f"\nError: {error}"

    @classmethod
    def setup_subparser(cls, parser, subparsers):
        name = cls.__name__.lower()
        aliases = getattr(cls, 'aliases', [])
        subparser = subparsers.add_parser(name, aliases=aliases)
        subparser.set_defaults(subcommand_cls=cls)
        cls.fill_subparser(parser, subparser)


class BaseBuildSubcommand(BaseSubcommand):
    __doc__ = '\n    Provides common functionality used by subcommands which build images\n    '
    rw_env = True
    remote_action = True
    update_version_env_vars = True

    def do_validate_profile(self):
        return False

    @classmethod
    def fill_subparser(cls, parser, subparser) -> None:
        pass

    def is_missing_env_arg_okay(self):
        return True

    @property
    @lru_cache()
    def compose(self):
        """
        Returns a Compose subcommand
        """
        from .compose import Compose
        return Compose(self.workflow)

    def build(self, pull=True):
        compose_args = [
         'build']
        if pull:
            compose_args.append('--pull')
        self.compose.handle(extra_args=compose_args)