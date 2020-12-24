# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pylxca/test/poc/fakegit.py
# Compiled at: 2019-12-05 00:54:38
import argparse, sys, re, shlex

class FakeGit(object):
    """
    Help for fakegit class
    """

    def __init__(self):
        """
        Help for init of fake git
        """
        parser = argparse.ArgumentParser(description=__doc__, usage='git <command> [<args>]\n\nThe most commonly used git commands are:\n   commit     Record changes to the repository\n   fetch      Download objects and refs from another repository\n   quit       quit shell\n')
        parser.add_argument('command', help='Subcommand to run')
        while True:
            astr = raw_input('$: ')
            try:
                args_list = shlex.split(astr)
                args = parser.parse_args(args_list[0:1])
            except SystemExit:
                print 'error'
                continue

            if not hasattr(self, args.command):
                print 'Unrecognized command'
                parser.print_help()
            elif args.command == 'help':
                parser.print_help()
            elif args.command == 'quit':
                break
            else:
                try:
                    getattr(self, args.command)(args_list)
                except SystemExit:
                    print 'I am herer '
                    continue

    def commit(self, args):
        """
        Help for commit overridden
        """
        parser = argparse.ArgumentParser(description='Record changes to the repository')
        parser.add_argument('--amend', action='store_true')
        args = parser.parse_args(args[1:])
        print 'Running git commit, amend=%s' % args.amend

    def fetch(self, args):
        """
                Help for fetch overridden
        """
        parser = argparse.ArgumentParser(description='Download objects and refs from another repository')
        parser.add_argument('repository')
        args = parser.parse_args(args[1:])
        print 'Running git fetch, repository=%s' % args.repository

    def quit(self):
        exit(0)


if __name__ == '__main__':
    FakeGit()