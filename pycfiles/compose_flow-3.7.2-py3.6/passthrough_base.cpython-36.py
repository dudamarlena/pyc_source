# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/compose_flow/commands/subcommands/passthrough_base.py
# Compiled at: 2020-05-06 10:05:57
# Size of source mod 2**32: 1600 bytes
import argparse, logging, os
from distutils.spawn import find_executable
from .base import BaseSubcommand
from compose_flow import errors

class PassthroughBaseSubcommand(BaseSubcommand):
    command_name = None

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)

    @classmethod
    def fill_subparser(cls, parser, subparser) -> None:
        subparser.add_argument('extra_args', nargs=(argparse.REMAINDER))

    def get_command(self):
        command_path = find_executable(self.command_name)
        if command_path is None:
            raise errors.ErrorMessage(f"{self.command_name} not found in PATH; is it installed?")
        return [
         command_path]

    def handle(self, extra_args: list=None, log_output: bool=False) -> [None, str]:
        command = self.get_command()
        args = self.workflow.args
        extra_args = extra_args or args.extra_args
        command.extend(extra_args)
        command_s = ' '.join([x if ' ' not in x else repr(x) for x in command])
        self.logger.info(command_s)
        if not args.dry_run:
            res = self.execute(command_s, _fg=True)
            if res:
                if log_output:
                    self.logger.info(res.stdout.decode('utf-8').strip())

    @property
    def logger(self) -> logging.Logger:
        return logging.getLogger(f"{__name__}.{self.__class__.__name__}")