# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/todd/github/restructuredtext-lint/restructuredtext_lint/cli.py
# Compiled at: 2018-11-14 01:01:57
from __future__ import absolute_import
import argparse
from collections import OrderedDict
import json, os, sys
from docutils.utils import Reporter
from restructuredtext_lint.lint import lint_file
WARNING_LEVEL_KEY = 'warning'
LEVEL_MAP = OrderedDict([
 (
  'debug', Reporter.DEBUG_LEVEL),
 (
  'info', Reporter.INFO_LEVEL),
 (
  WARNING_LEVEL_KEY, Reporter.WARNING_LEVEL),
 (
  'error', Reporter.ERROR_LEVEL),
 (
  'severe', Reporter.SEVERE_LEVEL)])
with open(os.path.join(os.path.dirname(__file__), 'VERSION'), 'r') as (version_file):
    VERSION = version_file.read().strip()
DEFAULT_FORMAT = 'text'
DEFAULT_LEVEL_KEY = WARNING_LEVEL_KEY

def _main(paths, format=DEFAULT_FORMAT, stream=sys.stdout, encoding=None, level=LEVEL_MAP[DEFAULT_LEVEL_KEY], **kwargs):
    error_dicts = []
    error_occurred = False
    filepaths = []
    for path in paths:
        if os.path.isfile(path):
            filepaths.append(path)
        else:
            for root, subdir, files in os.walk(path):
                for file in files:
                    if file.endswith('.rst'):
                        filepaths.append(os.path.join(root, file))

    for filepath in filepaths:
        unfiltered_file_errors = lint_file(filepath, encoding=encoding, **kwargs)
        file_errors = [ err for err in unfiltered_file_errors if err.level >= level ]
        if file_errors:
            error_occurred = True
            if format == 'text':
                for err in file_errors:
                    stream.write(('{err.type} {err.source}:{err.line} {err.message}\n').format(err=err))

            elif format == 'json':
                error_dicts.extend({'line': error.line, 'source': error.source, 'level': error.level, 'type': error.type, 'message': error.message, 'full_message': error.full_message} for error in file_errors)

    if format == 'json':
        stream.write(json.dumps(error_dicts))
    if error_occurred:
        sys.exit(2)
    else:
        sys.exit(0)


def main():
    parser = argparse.ArgumentParser(description='Lint reStructuredText files. Returns 0 if all files pass linting, 1 for an internal error, and 2 if linting failed.')
    parser.add_argument('--version', action='version', version=VERSION)
    parser.add_argument('paths', metavar='path', nargs='+', type=str, help='File/folder to lint')
    parser.add_argument('--format', default=DEFAULT_FORMAT, type=str, choices=('text',
                                                                               'json'), help=('Format of the output (default: "{default}")').format(default=DEFAULT_FORMAT))
    parser.add_argument('--encoding', type=str, help='Encoding of the input file (e.g. "utf-8")')
    parser.add_argument('--level', default=DEFAULT_LEVEL_KEY, type=str, choices=LEVEL_MAP.keys(), help=('Minimum error level to report (default: "{default}")').format(default=DEFAULT_LEVEL_KEY))
    parser.add_argument('--rst-prolog', type=str, help='reStructuredText content to prepend to all files (useful for substitutions)')
    args = parser.parse_args()
    args.level = LEVEL_MAP[args.level]
    _main(**args.__dict__)


if __name__ == '__main__':
    main()