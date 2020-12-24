# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/lib.linux-i686-2.7/ppu/find_executable.py
# Compiled at: 2017-06-04 15:18:28
import os, sys

def find_executable(executable, path=None):
    """Find if 'executable' can be run. Looks for it in 'path'
    (string that lists directories separated by 'os.pathsep';
    defaults to os.environ['PATH']). Checks for all executable
    extensions. Returns full path or None if no command is found.
    """
    if path is None:
        path = os.environ['PATH']
    paths = path.split(os.pathsep)
    extlist = ['']
    if os.name == 'os2':
        base, ext = os.path.splitext(executable)
        if not ext:
            executable = executable + '.exe'
    else:
        if sys.platform == 'win32':
            pathext = os.environ['PATHEXT'].lower().split(os.pathsep)
            base, ext = os.path.splitext(executable)
            if ext.lower() not in pathext:
                extlist = pathext
        for ext in extlist:
            execname = executable + ext
            if os.path.isfile(execname):
                return execname
            for p in paths:
                f = os.path.join(p, execname)
                if os.path.isfile(f):
                    return f

        else:
            return

    return


if __name__ == '__main__':
    print find_executable('git')