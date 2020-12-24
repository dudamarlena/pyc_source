# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\maha_cet_parser\main.py
# Compiled at: 2020-04-12 15:35:56
# Size of source mod 2**32: 452 bytes
"""Main entry point for pcd module"""
import sys, logging, maha_cet_parser.commands
logging.basicConfig(level=(logging.INFO))

def maha_cet_parser_tools_cli():
    """CLI entry point for the app"""
    sys.exit(cli_from_args(sys.argv[1:]))


def cli_from_args(args):
    args = maha_cet_parser.commands.Command.parse_args(args)
    return args.func(args)


if __name__ == '__main__':
    maha_cet_parser_tools_cli()