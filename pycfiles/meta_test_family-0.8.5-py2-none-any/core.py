# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/tmpujv2ur9q/0.8.5/meta-test-family-0.8.5/moduleframework/core.py
# Compiled at: 2018-09-27 08:43:14
from __future__ import print_function
import sys, os
DATADIR = [
 'usr', 'share', 'moduleframework']

def is_debug():
    """
    Return the **DEBUG** envvar.

    :return: bool
    """
    return bool(os.environ.get('DEBUG'))


def is_not_silent():
    """
    Return the opposite of the **DEBUG** envvar.

    :return: bool
    """
    return is_debug()


def print_info(*args):
    """
    Print information from the expected stdout and
    stderr files from the native test scope.

    See `Test log, stdout and stderr in native Avocado modules
    <https://avocado-framework.readthedocs.io/en/latest/WritingTests.html
    #test-log-stdout-and-stderr-in-native-avocado-modules>`_ for more information.

    :param args: object
    :return: None
    """
    for arg in args:
        print(arg, file=sys.stderr)


def print_debug(*args):
    """
    Print information from the expected stdout and
    stderr files from the native test scope if
    the **DEBUG** envvar is set to True.

    See `Test log, stdout and stderr in native Avocado modules
    <https://avocado-framework.readthedocs.io/en/latest/WritingTests.html
    #test-log-stdout-and-stderr-in-native-avocado-modules>`_ for more information.

    :param args: object
    :return: None
    """
    if is_debug():
        print_info(*args)