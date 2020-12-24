# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\daversy\dvs.py
# Compiled at: 2016-01-14 15:12:15
import os, sys
from daversy import VERSION
from daversy.command import Command

def main():
    cmd = os.path.basename(sys.argv[0])
    if len(sys.argv) == 1:
        print "Type '%s help' for usage." % cmd
        return
    if sys.argv[1] == 'help' and len(sys.argv) > 2:
        command = Command.get(sys.argv[2])
        if command:
            command.parser().print_help()
            return
    else:
        command = Command.get(sys.argv[1])
        if command:
            command(cmd, sys.argv[2:])
            return
    print DVS_HEADER % dict(cmd=cmd, version=VERSION)
    for command in Command.list():
        names = command.__names__
        print '  %s' % names[0],
        if len(names) > 1:
            print '(%s)' % (', ').join(names[1:])
        else:
            print

    print DVS_FOOTER


DVS_HEADER = "usage: %(cmd)s <subcommand> [options] [args]\nDaversy command-line client, version %(version)s.\nType '%(cmd)s help <subcommand>' for help on a specific subcommand.\n\nAvailable subcommands:\n"
DVS_FOOTER = '\nDaversy is a source control tool for relational databases.'
if __name__ == '__main__':
    sys.exit(main())