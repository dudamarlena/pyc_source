# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/empower_core/cli/help_commands/help.py
# Compiled at: 2020-05-10 06:49:24
# Size of source mod 2**32: 1316 bytes
"""Print help message."""
import argparse, sys
import empower_core.command as command

def pa_cmd(args, cmd):
    """ Help option parser. """
    usage = '%s <cmd>' % command.USAGE.format(cmd)
    args, leftovers = argparse.ArgumentParser(usage=usage).parse_known_args(args)
    return (args, leftovers)


def do_cmd(gargs, args, leftovers):
    """ Help execute method. """
    if len(leftovers) != 1:
        print('No command specified')
        command.print_available_cmds()
        sys.exit()
    try:
        parse_args, _ = command.CMDS[leftovers[0]]
        parse_args(['--help'], leftovers[0])
    except KeyError:
        print('Invalid command: %s is an unknown command.' % leftovers[0])
        sys.exit()