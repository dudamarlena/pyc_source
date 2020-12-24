# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/darpy/main.py
# Compiled at: 2017-11-03 16:11:32
from __future__ import print_function
from darpy.common import make_parser
from darpy.pack import add_pack_command
from darpy.unpack import add_unpack_command

def parse_args():
    parser, subparsers = make_parser()
    add_pack_command(subparsers)
    add_unpack_command(subparsers)
    return parser.parse_args()


def main():
    args = parse_args()
    args.func(args)


if __name__ == '__main__':
    main()