# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/johan/jpylyzer/jpylyzer/shared.py
# Compiled at: 2019-10-08 11:09:01
"""Shared functions for jpylyzer sub-modules."""
import sys

def printWarning(msg):
    """Print warning to stderr."""
    msgString = 'User warning: ' + msg + '\n'
    sys.stderr.write(msgString)


def errorExit(msg):
    """Print error message to stderr and exit."""
    msgString = 'Error: ' + msg + '\n'
    sys.stderr.write(msgString)
    sys.exit()


def consecutive(lst):
    """Return True if items in lst are consecutive numbers."""
    for i in range(1, len(lst)):
        if lst[i] - lst[(i - 1)] != 1:
            return False

    return True


def listOccurrencesAreContiguous(lst, value):
    """Return True if all occurrences of value in lst are at contiguous positions."""
    indices_of_value = [ i for i in range(len(lst)) if lst[i] == value ]
    return consecutive(indices_of_value)