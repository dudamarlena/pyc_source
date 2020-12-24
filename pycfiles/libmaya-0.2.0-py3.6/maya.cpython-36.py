# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/maya/exp_runner/maya.py
# Compiled at: 2019-06-13 05:22:46
# Size of source mod 2**32: 2573 bytes
import os, argparse, pkg_resources
from .maya_utils import run_batch
from colorama import init
init(autoreset=True)
__version__ = '0.2.0'
if os.environ.get('COVERAGE_PROCESS_START'):
    import coverage
    coverage.process_startup()

def maya_info(*args):
    if args[0].version:
        print(__version__)
    else:
        print('please run "maya {positional argument} --help" to see maya guidance')


def parse_args():
    """Definite the arguments users need to follow and input"""
    parser = argparse.ArgumentParser(prog='maya', description='use maya command to control nni experiments')
    parser.add_argument('--version', '-v', action='store_true')
    parser.set_defaults(func=maya_info)
    subparsers = parser.add_subparsers()
    parser_start = subparsers.add_parser('B', help='run command with multiprocess.')
    parser_start.add_argument('--command', '-c', required=True, dest='command', help='command to run')
    parser_start.add_argument('--source_dir', '-s', required=True, dest='source_dir', help='source dir')
    parser_start.add_argument('--target_dir', '-t', dest='target_dir', help='target dir')
    parser_start.add_argument('--debug', '-d', action='store_true', help='set debug mode')
    parser_start.set_defaults(func=run_batch)
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    parse_args()