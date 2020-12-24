# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snekchek/__main__.py
# Compiled at: 2020-03-03 07:34:32
"""
Linter/Styler/Checker combined for linters.

Linters supported:

- flake8
- flake8-bugbear (ext)
- flake8-import-order (ext)
- flake8-docstrings (ext)
- flake8-todo (ext)
- flake8-requirements (ext)
- flake8-string-format (ext)
- flake8-tidy-import (ext)
- flake8-bandit (ext, bandit)
- pylint
- yapf
- isort
- black
- pyroma
- safety
- bandit
- dodgy
- vulture
- pytest
- Upload to pypi
"""
from __future__ import absolute_import
import argparse, os
from snekchek.config_gen import generate
from snekchek.lint import get_linters
from snekchek.structure import CheckHandler
from snekchek.style import get_stylers

def run_main(args, do_exit=True):
    """Runs the checks and exits.

    To extend this tool, use this function and set do_exit to False
    to get returned the status code.
    """
    if args.init or not os.path.exists(args.config_file):
        generate()
        return None
    else:
        handler = CheckHandler(file=args.config_file, out_json=args.json, out_json_indent=args.json_indent, files=args.files)
        if args.skip_format:
            for style in get_stylers():
                handler.run_linter(style())

        for linter in get_linters():
            handler.run_linter(linter())

        from snekchek.secure import get_security
        from snekchek.tool import get_tools
        for security in get_security():
            handler.run_linter(security())

        for tool in get_tools():
            tool = tool()
            if tool.name == 'pypi' and handler.status_code != 0:
                continue
            handler.run_linter(tool)

        if do_exit:
            handler.exit()
        return handler.status_code


def main():
    """Main entry point for console commands."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--json', help='output in JSON format', action='store_true', default=False)
    parser.add_argument('--config-file', help='Select config file to use', default='.snekrc')
    parser.add_argument('files', metavar='file', nargs='*', default=[], help='Files to run checks against')
    parser.add_argument('--init', help='generate snekrc', action='store_true', default=False)
    parser.add_argument('--skip-format', help='skip formatters like isort and black', action='store_true', default=False)
    parser.add_argument('--json-indent', help='Indents to use for JSON', metavar='n', type=int, default=0)
    args = parser.parse_args()
    run_main(args)


if __name__ == '__main__':
    main()