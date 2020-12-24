# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/main/main.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 1131 bytes
import importlib, sys
from .. import commands

def main(argv=None):
    argv = sys.argv[1:] if argv is None else list(argv)
    for i, arg in enumerate(argv):
        if arg in commands.COMMANDS:
            command = argv.pop(i)
            break
    else:
        command = DEFAULT_COMMAND
        if all(a.startswith('-') for a in argv):
            from ..util import log
            if '-h' in argv or '--help' in argv:
                log.printer(USAGE)
                return 0
            log.error(ERROR + '\n\n' + USAGE)
            return -1

    module = importlib.import_module('bibliopixel.commands.' + command)
    if hasattr(module, 'main'):
        return module.main(argv)
    description = module.__doc__ + getattr(module, 'DESCRIPTION', '')
    from .args import set_args
    args = set_args(description, argv, module)
    module.run(args)


DEFAULT_COMMAND = 'run'
ERROR = 'No command entered!'
USAGE = 'Valid commands are:\n\n' + commands.COMMANDS_PRINTABLE + '\n\nFor help on each command, type\n\n    bp <command> --help\n\nor\n\n    bp <command> -h\n'
if __name__ == '__main__':
    sys.exit(main())