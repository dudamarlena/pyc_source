# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mfriszky/testest/env/lib/python3.6/site-packages/kontol/cli.py
# Compiled at: 2019-10-18 05:05:35
# Size of source mod 2**32: 1148 bytes
"""
Usage:
  kontol <command> [<args>...]

Options:
  -h, --help                             display this help and exit
  -v, --version                          Print version information and quit

Commands:
  masukin           Run Your Project

Run 'kontol COMMAND --help' for more information on a command.
"""
from inspect import getmembers, isclass
from docopt import docopt, DocoptExit
from kontol import __version__ as VERSION

def main():
    """Main CLI entrypoint."""
    import kontol.clis
    options = docopt(__doc__, version=VERSION, options_first=True)
    command_name = ''
    args = ''
    command_class = ''
    command_name = options.pop('<command>')
    args = options.pop('<args>')
    if args is None:
        args = {}
    try:
        module = getattr(kontol.clis, command_name)
        kontol.clis = getmembers(module, isclass)
        command_class = [command[1] for command in kontol.clis if command[0] != 'Base'][0]
    except AttributeError as e:
        print(e)
        raise DocoptExit()

    command = command_class(options, args)
    command.execute()


if __name__ == '__main__':
    main()