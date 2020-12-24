# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/climb/args.py
# Compiled at: 2015-05-23 15:45:28
# Size of source mod 2**32: 1668 bytes
import argparse
from collections import namedtuple
from climb.exceptions import UnknownCommand
Command = namedtuple('Command', ['name', 'parser'])

class ArgsParser(argparse.ArgumentParser):

    def error(self, message):
        raise UnknownCommand(self.format_help().strip())


class Args(object):

    def __init__(self, cli):
        self._cli = cli
        self._commands = []
        self._parser = ArgsParser(add_help=False)
        self._commands_parser = self._parser.add_subparsers(help='command')
        self._load_commands()
        help = self._add_command('help', 'show detailed help for command', parser=(self._parser),
          all_commands=(self._commands))
        help.add_argument('subject', nargs='?', default=None)
        self._add_command('exit', 'exit console')
        actions = [action for action in self._parser._actions if isinstance(action, argparse._SubParsersAction)]
        self._commands.extend([Command(choice, subparser) for action in actions for choice, subparser in action.choices.items()])

    def _load_commands(self):
        """Should be overridden by subclass."""
        pass

    def _add_command(self, name, help, **kwargs):
        command = self._commands_parser.add_parser(name, help=help, add_help=False)
        (command.set_defaults)(command=name, **kwargs)
        return command

    def parse(self, *args):
        return self._parser.parse_args(args)

    @property
    def commands(self):
        return self._commands