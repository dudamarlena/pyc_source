# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/plexshell/scripts/shell.py
# Compiled at: 2011-09-15 10:27:17
from plexshell import PlexShell
import argparse, os

def main():
    parser = argparse.ArgumentParser(description='A interactive command line PMS client')
    parser.add_argument('-H', '--host', metavar='hostname', nargs='?', default='localhost')
    parser.add_argument('-p', '--port', metavar='portno', nargs='?', type=int, default=32400)
    parser.add_argument('-s', '--script', metavar='scriptpath', nargs='?', default=None)
    args = parser.parse_args()
    stdin = None
    if args.script:
        if not os.path.isfile(args.script):
            print 'Script does not exist: %s' % args.script
            exit(1)
        stdin = open(args.script)
    client = PlexShell(args.host, args.port, stdin=stdin)
    client.cmdloop()
    return


if __name__ == '__main__':
    main()