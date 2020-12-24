# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /opt/griflet/venv/lib/python3.4/site-packages/pyrev/devel.py
# Compiled at: 2017-02-20 22:35:35
# Size of source mod 2**32: 3748 bytes
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from logging import getLogger, StreamHandler
from .main import lint
from .version import VERSION
from . import utils
import os, shutil, sys

def lintstr(args, logger):
    pass


def copy_document(args, logger):
    """
    Copy a chapter from source to dest. Also copies relevant images.

    src must be a specific file in a project
    dst can be a directory or a file, whose name may be different from
    the original.
    """
    return utils.copy_document(args.src, args.dst, logger)


def move_document(args, logger):
    """
    Copy a chapter from source to dest. Also copies relevant images.

    src must be a specific file in a project
    dst can be a directory or a file, whose name may be different from
    the original.
    """
    return utils.move_document(args.src, args.dst, logger)


def devel():
    """
    Another entrance for pyrev. Available with pyrev-devel.
    """
    parser = ArgumentParser(description=__doc__, formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('--log', default='INFO', help='Set log level. e.g. DEBUG, INFO, WARN')
    parser.add_argument('-d', '--debug', action='store_true', help='Aliased to --log=DEBUG')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s {}'.format(VERSION), help='Show version and exit.')
    subparsers = parser.add_subparsers()
    parser_lint = subparsers.add_parser('lint', help='Do lint check')
    parser_lint.add_argument('filename')
    parser_lint.add_argument('-u', '--unacceptable_level', action='store', default='CRITICAL', help='Error level that aborts the check.')
    parser_lint.set_defaults(func=lint)
    parser_lintstr = subparsers.add_parser('lintstr', help='Check a given string')
    parser_lintstr.set_defaults(func=lintstr)
    parser_ic = subparsers.add_parser('copy-document', help='Copy a single document')
    parser_ic.add_argument('src')
    parser_ic.add_argument('dst')
    parser_ic.set_defaults(func=copy_document)
    parser_ic = subparsers.add_parser('move-document', help='Move a single document')
    parser_ic.add_argument('src')
    parser_ic.add_argument('dst')
    parser_ic.set_defaults(func=move_document)
    args = parser.parse_args()
    if args.debug:
        args.log = 'DEBUG'
    logger = getLogger(__name__)
    handler = StreamHandler()
    logger.setLevel(args.log.upper())
    handler.setLevel(args.log.upper())
    logger.addHandler(handler)
    return args.func(args, logger)


if __name__ == '__main__':
    ret = devel()
    if ret != 0:
        sys.exit(ret)