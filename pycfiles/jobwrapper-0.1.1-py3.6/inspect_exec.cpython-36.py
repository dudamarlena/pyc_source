# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jobwrapper/inspect_exec.py
# Compiled at: 2018-09-07 06:00:00
# Size of source mod 2**32: 1275 bytes
"""This module helps to inspect an executable.
In particulare:
1. If it has been compiled with debug option `_g`
2.
"""
import subprocess as sbp, os.path

def is_debug(root=b'./', execname=b'lppic', verbose=True):
    """ return True if the executable has been compiled with debug """
    fname = root + execname
    if verbose:
        print('Inspecting the debug option of the executable')
        print('File name:', fname)
        print('=======================')
    if not os.path.isfile(fname):
        if verbose:
            print('the executable do not existe ! Check your location or arguments')
        return
    p = sbp.run(['gdb', root + execname], input=b'q', stdout=(sbp.PIPE))
    iout = p.stdout.strip()
    lines = iout.decode('ascii').splitlines()
    line = lines[(-3)]
    info = line[-35:-9]
    if info == 'no debugging symbols found':
        if verbose:
            print('The executable is runing without the debug option')
        return False
    else:
        if verbose:
            print('This executable is running with the debug option `-g`')
        return True


if __name__ == '__main__':
    if is_debug(verbose=True):
        print('True')
    else:
        print('False')