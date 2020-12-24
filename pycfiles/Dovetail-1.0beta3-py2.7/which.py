# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/dovetail/util/which.py
# Compiled at: 2012-08-01 03:51:57
"""A multi-platform implementation of the Unix 'which' command in Python."""
from os import environ, path, access, pathsep

def which(program):
    """A Python implementation of the Unix 'which' command, which tests whether
    the argument is a program either directly accessible or is on the system path.

    :param program: The name of a file that should be on the path
    :type program: string
    :return: The full path of the first executable found, or None    if the executable is not on the path
    :rtype: string
    """

    def is_exe(filepath):
        """Returns *True* if filepath is an executable"""
        from os import X_OK
        return path.isfile(filepath) and access(filepath, X_OK)

    entry, _ = path.split(program)
    if entry:
        if is_exe(program):
            return program
    else:
        for entry in environ['PATH'].split(pathsep):
            exe_file = path.join(entry, program)
            if is_exe(exe_file):
                return exe_file

    return