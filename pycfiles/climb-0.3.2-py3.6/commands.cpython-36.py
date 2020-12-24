# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/climb/commands.py
# Compiled at: 2015-06-07 05:01:24
# Size of source mod 2**32: 1464 bytes
from climb.exceptions import UnknownCommand

def command(function):
    function.command = True
    return function


def completers(*compl):

    def wrapper(function):
        function.completers = compl
        return function

    return wrapper


class Commands(object):

    def __init__(self, cli):
        self._cli = cli
        self._commands = {}

    def execute(self, name, *args, **kwargs):
        if hasattr(self, name):
            method = getattr(self, name)
            if getattr(method, 'command', None):
                return method(*args, **kwargs)
        raise UnknownCommand('There is no action for command {}'.format(command))

    def get_completer(self, name, position):
        if hasattr(self, name):
            method = getattr(self, name)
            compl = getattr(method, 'completers', [])
            if compl:
                pos = position - 1
                if len(compl) > pos:
                    return compl[pos]
                return compl[0]
        raise UnknownCommand('No completer for command {}'.format(command))

    @command
    def help(self, parser, all_commands, subject):
        if subject:
            subparsers = [cmd for cmd in all_commands if cmd.name == subject]
            if subparsers:
                parser = subparsers[0].parser
        return parser.print_help()

    @command
    def exit(self):
        self._cli.set_running(False)