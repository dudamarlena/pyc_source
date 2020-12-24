# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/print/argparse.py
# Compiled at: 2019-02-25 18:20:32
__doc__ = 'Basic argument parsing utilities'
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