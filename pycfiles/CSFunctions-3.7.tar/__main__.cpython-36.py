# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/csft/__main__.py
# Compiled at: 2018-01-15 11:14:49
# Size of source mod 2**32: 1649 bytes
__doc__ = '\nThe entry point of csft.\n'
from __future__ import print_function
import sys
from argparse import ArgumentParser
from os.path import curdir
from pathlib import Path
from humanfriendly import format_size
from . import __name__ as _name, __version__ as _version
from ._csft import column, csft2data

def _dir(path_str):
    path = Path(path_str)
    if not path.is_dir():
        raise TypeError('%s is not a directory!', path_str)
    else:
        return path


def _positive_int(num):
    number = int(num)
    if number <= 0:
        raise ValueError('%s is not positive!', number)
    return number


def _parse_args(argv):
    parser = ArgumentParser(prog=_name)
    parser.add_argument('-V', '--version', action='version', version=_version)
    parser.add_argument('path', type=_dir, help='the directory to be analyzed')
    parser.add_argument('--top', type=_positive_int, metavar='N', help='only display top N results')
    parser.add_argument('--with-raw', action='store_true', help='print raw size without units')
    return parser.parse_args(args=argv)


def main(argv=None):
    """Execute the application from CLI."""
    if argv is None:
        argv = sys.argv[1:]
    else:
        if not argv:
            argv = [
             curdir]
        args = _parse_args(argv)
        data = csft2data(args.path)
        if args.top:
            data = data.head(args.top)
        if args.with_raw:
            data['raw'] = data[column.SIZE]
    data[column.SIZE] = data[column.SIZE].map(format_size)
    print(data)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())