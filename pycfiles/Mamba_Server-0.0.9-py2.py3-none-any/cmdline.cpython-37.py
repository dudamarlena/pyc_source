# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/argos/Workspace/mamba-framework/mamba-server/mamba_server/cmdline.py
# Compiled at: 2020-05-12 03:57:45
# Size of source mod 2**32: 1685 bytes
import sys, optparse, mamba_server
from mamba_server.commands import MambaCommand
from mamba_server.utils.misc import get_classes_from_module

def _pop_command_name(argv):
    i = 0
    for arg in argv[1:]:
        if not arg.startswith('-'):
            del argv[i]
            return arg
            i += 1


def _print_header():
    print('Mamba {}\n'.format(mamba_server.__version__))


def _print_commands():
    _print_header()
    print('Usage:')
    print('  mamba <command> [args]\n')
    print('Available commands:')
    cmds = get_classes_from_module('mamba_server.commands', MambaCommand)
    for cmdname, cmdclass in sorted(cmds.items()):
        print('  %-13s %s' % (cmdname, cmdclass.short_desc()))

    print()
    print('Use "mamba <command> -h" to see more info about a command')


def _print_unknown_command(cmdname):
    _print_header()
    print('Unknown command: %s\n' % cmdname)
    print('Use "mamba" to see available commands')


def execute(argv=None):
    if argv is None:
        argv = sys.argv
    else:
        cmds = get_classes_from_module('mamba_server.commands', MambaCommand)
        cmdname = _pop_command_name(argv)
        parser = optparse.OptionParser(formatter=(optparse.TitledHelpFormatter()), conflict_handler='resolve')
        if not cmdname:
            _print_commands()
            sys.exit(0)
        else:
            if cmdname not in cmds:
                _print_unknown_command(cmdname)
                sys.exit(2)
    cmd = cmds[cmdname]
    parser.usage = 'mamba %s %s' % (cmdname, cmd.syntax())
    parser.description = cmd.long_desc()
    opts, args = parser.parse_args(args=(argv[1:]))
    cmd.run(argv[1:])


if __name__ == '__main__':
    execute()