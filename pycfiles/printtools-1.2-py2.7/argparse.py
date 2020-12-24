# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/print/argparse.py
# Compiled at: 2019-02-25 18:20:32
"""Basic argument parsing utilities"""
import sys

def is_char_flag(flag):
    """Check if character is flag"""
    for arg in sys.argv:
        if arg[0] == '-' and flag in arg[1:]:
            return True

    return False


def is_word_flag(flag):
    """Check if word is flag"""
    for arg in sys.argv:
        if arg == '--' + flag:
            return True

    return False


def is_flag(flag):
    """Check if flag is in arguments

    Parameters
    ----------
    flag : str
        If len(flag) == 1, searches for char flag; otherwise, searches for
        word length flag

    Returns
    -------
    bool
        True if flag is present
    """
    if len(flag) == 1:
        return is_char_flag(flag)
    else:
        return is_word_flag(flag)


def get_arg(flag):
    """Get argument following flag

    Parameters
    ----------
    flag : str
        Target flag

    Returns
    -------
    str or None
        Found argument; None if not found
    """
    for idx, arg in enumerate(sys.argv):
        if arg == '-' + flag and len(sys.argv) > idx + 1:
            return sys.argv[(idx + 1)]

    return