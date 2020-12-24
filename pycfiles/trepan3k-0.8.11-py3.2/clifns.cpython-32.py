# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/clifns.py
# Compiled at: 2017-08-10 07:59:32
import os, linecache, os.path as osp

def is_ok_line_for_breakpoint(filename, lineno, errmsg_fn):
    """Check whether specified line seems to be executable.

    Return `lineno` if it is, 0 if not (e.g. a docstring, comment, blank
    line or EOF). Warning: testing is not comprehensive.
    """
    line = linecache.getline(filename, lineno)
    if not line:
        errmsg_fn('End of file')
        return False
    line = line.strip()
    if not line or line[0] == '#' or line[:3] == '"""' or line[:3] == "'''":
        errmsg_fn('Blank or comment')
        return False
    return True


def file2module(filename):
    """Given a file name, extract the most likely module name. """
    basename = osp.basename(filename)
    if '.' in basename:
        pos = basename.rfind('.')
        return basename[:pos]
    else:
        return basename
        return


def search_file(filename, directories, cdir):
    """Return a full pathname for filename if we can find one. path
    is a list of directories to prepend to filename. If no file is
    found we'll return None"""
    for trydir in directories:
        if trydir == '$cwd':
            trydir = '.'
        elif trydir == '$cdir':
            trydir = cdir
        tryfile = osp.realpath(osp.join(trydir, filename))
        if osp.isfile(tryfile):
            return tryfile

    return


def whence_file(py_script, dirnames=None):
    """Do a shell-like path lookup for py_script and return the results.
    If we can't find anything return py_script"""
    if py_script.find(os.sep) != -1:
        return py_script
    else:
        if dirnames is None:
            dirnames = os.environ['PATH'].split(os.pathsep)
        for dirname in dirnames:
            py_script_try = osp.join(dirname, py_script)
            if osp.exists(py_script_try):
                return py_script_try

        return py_script


def path_expanduser_abs(filename):
    return os.path.abspath(os.path.expanduser(filename))


if __name__ == '__main__':
    import sys
    print(file2module(sys.argv[0]), sys.argv[0])
    ok = is_ok_line_for_breakpoint(__file__, 1, sys.stdout.write)
    print('\nCan stop at line 1? ', ok)
    ok = is_ok_line_for_breakpoint(__file__, 2, sys.stdout.write)
    print('\nCan stop at line 2? ', ok)
    print(path_expanduser_abs('./.trepan3krc'))
    print(path_expanduser_abs('~/.trepan3krc'))