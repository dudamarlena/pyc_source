# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spl/cli.py
# Compiled at: 2016-12-14 09:20:04
# Size of source mod 2**32: 1710 bytes
import importlib, pkgutil, sys, spl.commands as commands
from argparse import ArgumentParser
from spl.metadata import NAME, VERSION
from spl.errors import CannotGetStateLockException, ExitCode
from spl.spiget import SpiGet
COMMANDS = [m for _, m, _ in pkgutil.walk_packages(commands.__path__) if m[0] != '_']

def main(argv=None):
    """Command line options."""
    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)
    parser = ArgumentParser()
    parser.add_argument('-V', '--version', action='version', version='{} v{}'.format(NAME, VERSION))
    subparsers = parser.add_subparsers()
    for command in COMMANDS:
        subparser = subparsers.add_parser(command)
        command_module = importlib.import_module('spl.commands.{}'.format(command))
        if hasattr(command_module, 'add_parser_args') and hasattr(command_module, 'run'):
            command_module.add_parser_args(subparser)
            subparser.set_defaults(func=command_module.run)

    args = parser.parse_args()
    if args.func:
        try:
            spiget = SpiGet()
            return args.func(spiget, args).value
        except CannotGetStateLockException:
            print('Cannot obtain lock (is another spl process running?)')
            return ExitCode.CANNOT_GET_STATE_LOCK.value

    else:
        print('Unrecognised action: {}'.format(args.command))
        print('Available actions: {}'.format(COMMANDS))
        return ExitCode.UNKNOWN_COMMAND.value
    return ExitCode.OK.value


if __name__ == '__main__':
    sys.exit(main().value)