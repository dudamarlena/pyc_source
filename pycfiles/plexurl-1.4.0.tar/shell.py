# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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