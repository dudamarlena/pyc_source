# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Seth/Programming/input_reader/input_reader/files.py
# Compiled at: 2014-03-01 14:21:20
"""This is a collection of subroutines that are used at the start of
execution of a program, typically when processing files or command-
line arguements.
"""
from __future__ import unicode_literals
from os.path import abspath, expanduser, expandvars, join
from os import environ

def abs_file_path(filename, env=False):
    """    This function takes a *filename* and returns the absolute path.

    The reason this was written is that :py:func:`os.path.abspath`
    can convert a relative path, :py:func:`os.path.expandvars`
    can expand a shell variable, and :py:func:`os.path.expanduser`
    understands ~, but none of these does all three.  This function
    piggybacks the three of these to guaruntee any path will be
    returned absolutely.

    :argument filename:
        The path of the file that you wish to have the absolute
        path of.
    :type filename: str
    :argument env:
        Replace the base part of the path with $HOME, if that is
        where the path is.  The default is False.
    :type env: bool, optional
    :rtype: :py:obj:`str`
    """
    absfile = abspath(expandvars(expanduser(filename)))
    if env:
        if environ[b'HOME'] in absfile:
            i = len(environ[b'HOME']) + 1
            absfile = join(b'$HOME', absfile[i:])
    return absfile


def file_safety_check(filename):
    """    Function to check a file and raise an :py:exc:`IOError`
    if it is not "safe."  "Safe" meaning that the file exists and
    it is readable.

    :argument filename:
        The file you wish to check the safety of.
    :type filename: str
    :rtype: None
    :exception:
        :py:exc:`IOError` : Raised when a file is not safe
    """
    with open(filename) as (f):
        pass