# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/pygenprop/lib.py
# Compiled at: 2019-04-06 16:48:05
# Size of source mod 2**32: 427 bytes
"""
Created by: Lee Bergstrand (2017)

Description: A set of helper functions.
"""
from os import path

def sanitize_cli_path(cli_path):
    """
    Performs expansion of '~' and shell variables such as "$HOME" into absolute paths.

    :param cli_path: The path to expand
    :return: An expanded path.
    """
    sanitized_path = path.expanduser(path.expandvars(cli_path))
    return sanitized_path