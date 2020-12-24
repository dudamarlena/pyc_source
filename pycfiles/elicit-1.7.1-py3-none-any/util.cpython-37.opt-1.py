# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /elicit/util.py
# Compiled at: 2018-08-13 00:06:39
# Size of source mod 2**32: 1213 bytes
"""
Miscellaneous utility functions.
"""
import os, glob

def globargv(argv):
    """Expand all arguments in argv, all of glob charaters, environment
    variables, and user shorthand. Return a new list with what can be exanded so
    expanded, and those that can't are added as-is.
    """
    if len(argv) > 1:
        newargv = [
         argv[0]]
        for rawarg in argv[1:]:
            arg = os.path.expandvars(os.path.expanduser(rawarg))
            gl = glob.has_magic(arg) and glob.glob(arg) or [arg]
            newargv.extend(gl)

        return newargv
    return argv