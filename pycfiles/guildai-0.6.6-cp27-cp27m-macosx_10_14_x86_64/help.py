# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./guild/external/pip/_internal/commands/help.py
# Compiled at: 2019-09-10 15:18:29
from __future__ import absolute_import
from pip._internal.basecommand import SUCCESS, Command
from pip._internal.exceptions import CommandError

class HelpCommand(Command):
    """Show help for commands"""
    name = 'help'
    usage = '\n      %prog <command>'
    summary = 'Show help for commands.'
    ignore_require_venv = True

    def run(self, options, args):
        from pip._internal.commands import commands_dict, get_similar_commands
        try:
            cmd_name = args[0]
        except IndexError:
            return SUCCESS

        if cmd_name not in commands_dict:
            guess = get_similar_commands(cmd_name)
            msg = [
             'unknown command "%s"' % cmd_name]
            if guess:
                msg.append('maybe you meant "%s"' % guess)
            raise CommandError((' - ').join(msg))
        command = commands_dict[cmd_name]()
        command.parser.print_help()
        return SUCCESS