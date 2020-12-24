# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Python/2.7/site-packages/ctznosx/cli.py
# Compiled at: 2014-08-24 11:57:53
from __future__ import unicode_literals
import argparse, locale, sys
from os import listdir, walk, path, environ
from ctznosx import __version__, monitors as Monitors, devicemgmt as Manager
from ctznosx import report as Report
from ctznosx.exceptions import Error
from ctznosx.usage import *
from ctznosx import launcher
from config import ctznConfig
CTZNOSX_PATH = environ.get(b'CTZNOSX_PATH') or b'/var/lib/ctznosx/'
CTZNOSX_CONFIG = path.join(b'/etc/', b'ctznosx.conf')
CONFIG = ctznConfig(CTZNOSX_CONFIG, CTZNOSX_PATH)

def argument_parser(*args, **kwargs):
    format_usage = kwargs.pop(b'format_usage', None)
    format_help = kwargs.pop(b'format_help', None)

    class ArgumentParser(argparse.ArgumentParser):

        def format_usage(self):
            return b'%s\n' % format_usage

        def format_help(self):
            return b'%s\n%s\n' % (self.format_usage(), format_help)

    kwargs[b'add_help'] = False
    p = ArgumentParser(*args, **kwargs)
    p.add_argument(b'--help', action=b'help')
    p.add_argument(b'-h', action=b'help')
    return p


def monitor(args):
    if args is None:
        print MONITOR_USAGE
        sys.exit(1)
    elif args[1] in ('list', 'install', 'remove', 'upgrade'):
        getattr(Monitors, args[1])(args[2:])
    return


def manager(args):
    if args is None:
        print MANAGER_USAGE
        sys.exit(1)
    elif args[1] in b'register':
        Manager.register_device()
    return


def clean(args):
    print args


def main(argv=None):
    """
    Handle command line arguments.
    """
    if argv is None:
        argv = sys.argv[1:]
        encoding = locale.getdefaultlocale()[1]
        if encoding:
            argv = [ a.decode(encoding) for a in sys.argv[1:] ]
    pos, skip_next = 0, False
    for i, arg in enumerate(argv):
        if skip_next:
            skip_next = False
            continue
        else:
            pos = i
            break

    parser = argument_parser(prog=b'ctznosx', format_usage=USAGE, format_help=HELP)
    parser.add_argument(b'--verbose', action=b'store_true')
    parser.add_argument(b'--dry-run', action=b'store_true')
    parser.add_argument(b'--version', action=b'version', version=__version__)
    parser.add_argument(b'-v', action=b'version', version=__version__)
    parser.add_argument(b'command')
    try:
        args = parser.parse_args(argv[:pos + 1])
        if args.command in b'monitor':
            monitor(argv)
        elif args.command in b'manager':
            manager(argv)
        elif args.command in b'clean':
            clean(args)
        elif args.command in b'report':
            Report.run(argv)
        else:
            launcher.run()
    except Error as error:
        message = b'%s' % error
        if not message.endswith(b'\n'):
            message += b'\n'
        parser.exit(1, message)

    return