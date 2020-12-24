# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/pygenprop/lib.py
# Compiled at: 2019-04-06 16:48:05
# Size of source mod 2**32: 427 bytes
__doc__ = '\nCreated by: Lee Bergstrand (2017)\n\nDescription: A set of helper functions.\n'
from os import path

def sanitize_cli_path(cli_path):
    """
    Performs expansion of '~' and shell variables such as "$HOME" into absolute paths.

    :param cli_path: The path to expand
    :return: An expanded path.
    """
    sanitized_path = path.expanduser(path.expandvars(cli_path))
    return sanitized_path