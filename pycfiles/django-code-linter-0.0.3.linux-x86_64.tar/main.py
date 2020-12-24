# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/djinter/main.py
# Compiled at: 2014-05-08 09:09:50
import argparse, sys
from djinter import __version__
from djinter.lint import lint_project

def main(prog=None):
    parser = argparse.ArgumentParser(prog=prog, version=__version__)
    parser.add_argument('paths', nargs='+')
    args = parser.parse_args()
    results = []
    exit_code = 0
    for path in args.paths:
        results.extend(lint_project(path))

    for result in results:
        if result.get('severity') == 'critical':
            sys.stderr.write('%s\n' % result['message'])
            exit_code = 101

    sys.exit(exit_code)