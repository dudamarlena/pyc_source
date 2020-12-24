# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-sin1koo5/pip/pip/_internal/cli/main_parser.py
# Compiled at: 2019-07-30 18:46:55
# Size of source mod 2**32: 2817 bytes
"""A single place for constructing and exposing the main parser
"""
import os, sys
from pip._internal.cli import cmdoptions
from pip._internal.cli.parser import ConfigOptionParser, UpdatingDefaultsHelpFormatter
from pip._internal.commands import commands_dict, get_similar_commands, get_summaries
from pip._internal.exceptions import CommandError
from pip._internal.utils.misc import get_pip_version, get_prog
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
if MYPY_CHECK_RUNNING:
    from typing import Tuple, List
__all__ = ['create_main_parser', 'parse_command']

def create_main_parser():
    """Creates and returns the main parser for pip's CLI
    """
    parser_kw = {'usage':'\n%prog <command> [options]', 
     'add_help_option':False, 
     'formatter':UpdatingDefaultsHelpFormatter(), 
     'name':'global', 
     'prog':get_prog()}
    parser = ConfigOptionParser(**parser_kw)
    parser.disable_interspersed_args()
    parser.version = get_pip_version()
    gen_opts = cmdoptions.make_option_group(cmdoptions.general_group, parser)
    parser.add_option_group(gen_opts)
    parser.main = True
    command_summaries = get_summaries()
    description = [''] + ['%-27s %s' % (i, j) for i, j in command_summaries]
    parser.description = '\n'.join(description)
    return parser


def parse_command(args):
    parser = create_main_parser()
    general_options, args_else = parser.parse_args(args)
    if general_options.version:
        sys.stdout.write(parser.version)
        sys.stdout.write(os.linesep)
        sys.exit()
    if not args_else or args_else[0] == 'help' and len(args_else) == 1:
        parser.print_help()
        sys.exit()
    cmd_name = args_else[0]
    if cmd_name not in commands_dict:
        guess = get_similar_commands(cmd_name)
        msg = [
         'unknown command "%s"' % cmd_name]
        if guess:
            msg.append('maybe you meant "%s"' % guess)
        raise CommandError(' - '.join(msg))
    cmd_args = args[:]
    cmd_args.remove(cmd_name)
    return (
     cmd_name, cmd_args)