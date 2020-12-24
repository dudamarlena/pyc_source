# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/titan/cli.py
# Compiled at: 2014-10-17 09:40:47
from __future__ import unicode_literals
import argparse, locale, sys
from os.path import join
from os import listdir, walk, path, environ
from titan import __version__, monitors as Monitors, devicemgmt as Manager, report as Report
from titan.exceptions import Error
from titan.usage import *
from titan import launcher
from config import titanConfig
TITAN_PATH = environ.get(b'TITAN_PATH') or b'/var/lib/titan/'
TITAN_CONFIG = join(b'/etc/', b'titan.conf')
CONFIG = titanConfig(TITAN_CONFIG, TITAN_PATH)

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
    if args is None or len(args) == 1:
        print MONITOR_USAGE
        sys.exit(1)
    elif args[1] in ('list', 'install', 'remove', 'upgrade'):
        getattr(Monitors, args[1])(args[2:])
    else:
        print MONITOR_USAGE
        sys.exit(1)
    return


def manager(args):
    if args is None or len(args) == 1:
        print MANAGER_USAGE
        sys.exit(1)
    elif args[1] == b'register':
        Manager.register()
    elif args[1] == b'unregister':
        Manager.unregister()
    elif args[1] == b'status':
        Manager.status()
    else:
        print MANAGER_USAGE
        sys.exit(1)
    return


def clean(args):
    pass


def main(argv=None):
    """
    Handle command line arguments.
    """
    if argv is None:
        argv = sys.argv[1:]
    pos, skip_next = 0, False
    for i, arg in enumerate(argv):
        if skip_next:
            skip_next = False
            continue
        else:
            pos = i
            break

    parser = argument_parser(prog=b'titanosx', format_usage=USAGE, format_help=HELP)
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
        elif args.command in b'run':
            launcher.run()
        else:
            print USAGE
            sys.exit(1)
    except Error as error:
        message = b'%s' % error
        if not message.endswith(b'\n'):
            message += b'\n'
        parser.exit(1, message)

    return