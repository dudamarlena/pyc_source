# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\diskspace\diskspace.py
# Compiled at: 2019-12-20 08:41:26
# Size of source mod 2**32: 2325 bytes
import shlex, diskspace, argparse, re
from . import argpar, utils, pathRender

def shell():
    arguments = argpar.getarg()
    parser = argpar.Arguments(description='Making it possible to use Linux df & du command on Windows', add_help=False)
    parser.add_argument('--help', action='help', default=(argparse.SUPPRESS), help='Show this help message and exit.')
    parser.add_argument('-v', '--version', action='store_true', help='Show the version number and exit')
    parser.add_argument('-bl', '--blacklist', nargs='+', help='Exclude name or file extensions matching arguments', default=None)
    parser.add_argument('-wl', '--whitelist', nargs='+', help='Only include name or file extensions matching arguments', default=None)
    parser.add_argument('-h', '--human', action='store_true', help='Convert bytes in to readable format')
    parser.add_argument('-nf', '--nofolders', action='store_true', help='Ingore folders')
    parser.add_argument('-p', '--path', nargs='+', help='Choose a different path to check diskspace')
    parser.add_argument('-ns', '--nostats', action='store_true', help="Don't display disk space at top")
    try:
        arguments = arguments.replace('\\', '/')
        args = parser.parse_args(shlex.split(arguments))
    except Exception as e:
        try:
            utils.exitcode(e)
        finally:
            e = None
            del e

    if args.version:
        utils.exitcode(f"DiskSpace version: {diskspace.__version__}")
    else:
        nofolders = False if args.nofolders else True
        nostats = False if args.nostats else True
        if args.path:
            custom_path = ' '.join(args.path)
            custom_path = re.compile('^[A-Za-z]:\\/|^\\/').search(custom_path) or './' + ' '.join(args.path)
        else:
            custom_path = '.'
    if args.blacklist:
        if args.whitelist:
            utils.exitcode("You can't define blacklist/whitelist alone.")
    print(pathRender.ShowPath(path=custom_path,
      include_folder=nofolders,
      include_stats=nostats,
      whitelist=(args.whitelist),
      blacklist=(args.blacklist),
      human=(args.human)).pretty_print)


def main():
    try:
        shell()
    except KeyboardInterrupt:
        print('\nCancelling...')


if __name__ == '__main__':
    main()