# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/benchline/files.py
# Compiled at: 2014-03-23 21:02:31
"""
Methods to interact with directories.
"""
import os, random, benchline.args

def dir_file_in(file_name):
    """Returns the OS directory where file_name resides.
    To return the directory of the current file use __file__ as
    file_name.

    >>> filename = str(random.random())
    >>> cwd = os.getcwd()
    >>> open(filename, "w").close()
    >>> dir_file_in(filename) == cwd
    True
    >>> os.remove(filename)
    """
    return os.path.dirname(os.path.realpath(file_name))


if __name__ == '__main__':
    benchline.args.go(__doc__)