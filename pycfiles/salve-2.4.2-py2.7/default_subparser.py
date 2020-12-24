# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/salve/cli/default_subparser.py
# Compiled at: 2015-11-14 16:26:10
"""
The contents of this module are shamelessly stolen from ruamel's std.argparse
package: https://pypi.python.org/pypi/ruamel.std.argparse/0.6.0
Because std.argparse is MIT licensed, I'm not including licensing and copyright
information inline here -- it's available in the project's repo.

We want to do parsing with argparse, but we also want a behavior that argparse
doesn't have: defaulting to 'deploy' if no subcommand is present.

Some slight modifications have been made:
 - I've made this a function that takes a parser argument, rather than a class
   method for parsers.
 - There is no support for an 'args' kwarg
 - Simpler check for '--help' argument
 - Only slices sys.argv once, rather than once per arg (just feels cleaner to
   me)
"""
import sys, argparse

def set_default_subparser(parser, name):
    """
    Default subparser selection. Call after setup, just before parse_args()
    """
    subparser_found = False
    opts = sys.argv[1:]
    if '-h' in opts or '--help' in opts:
        return
    for x in parser._subparsers._actions:
        if not isinstance(x, argparse._SubParsersAction):
            continue
        for sp_name in x._name_parser_map.keys():
            if sp_name in opts:
                subparser_found = True

    if not subparser_found:
        sys.argv.insert(1, name)