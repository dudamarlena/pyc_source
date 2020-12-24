# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/thejoeejoee/projects/VUT-FIT-IFJ-2017-tests/ifj2017/test/main.py
# Compiled at: 2017-12-06 08:33:00
# Size of source mod 2**32: 2507 bytes
import platform
from argparse import ArgumentParser
from os import path
import ifj2017
from ifj2017 import __PROJECT_ROOT__
from ifj2017.test.runner import TestRunner

def main():
    parser = ArgumentParser(description='Automatic test cases runner for IFJ17 compiler.', epilog='\n        Authors: Josef Kolář (xkolar71, @thejoeejoee), Son Hai Nguyen (xnguye16, @SonyPony), GNU GPL v3, 2017\n        ')
    if not TestRunner.check_platform():
        exit(1)
    parser.add_argument('compiler', help='path to IFJ17 compiler binary')
    parser.add_argument('tests', nargs='*', help='wildcards to specify, which sections/tests run', default=[])
    parser.add_argument('-i', '--interpreter', help='path to IFJ17 interpreter binary', type=str, default=TestRunner.INTERPRETERS.get(platform.system()))
    parser.add_argument('-e', '--extensions-file', help="path to file with extensions 'rozsireni'")
    parser.add_argument('-v', '--verbose', help='enable verbose output', default=False, action='store_true')
    parser.add_argument('--no-interpreter', help='disable interpretation by ic17int', default=False, action='store_true')
    parser.add_argument('-d', '--tests-dir', help='path to folder with tests to run', type=str, default=path.join(__PROJECT_ROOT__, 'ifj2017/tests'))
    parser.add_argument('-l', '--log-dir', help='path to folder with logs', type=str)
    parser.add_argument('-t', '--token-file', help='path to token file (default .TOKEN in log dir)', type=str)
    parser.add_argument('--benchmark-url-target', help='target hostname to send benchmark results', type=str, default='https://ifj.josefkolar.cz')
    parser.add_argument('--command-timeout', help='maximal timeout for compiler and interpreter', type=float, default=0.25)
    parser.add_argument('--no-colors', action='store_true', help='disable colored output (for Windows CMD etc.)', default=False)
    parser.add_argument('--no-stdout-diff', action='store_true', help='disable stdout log by difflib', default=False)
    parser.add_argument('-V', '--version', action='version', version='%(prog)s {}'.format(ifj2017.__version__))
    runner = TestRunner(parser.parse_args())
    return runner.run()