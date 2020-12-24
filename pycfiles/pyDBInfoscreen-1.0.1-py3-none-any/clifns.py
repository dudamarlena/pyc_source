# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/clifns.py
# Compiled at: 2013-03-11 06:01:52
import os, linecache
from import_relative import import_relative
Mfile = import_relative('file', '.lib')

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
    basename = os.path.basename(filename)
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
        tryfile = os.path.abspath(os.path.join(trydir, filename))
        if os.path.isfile(tryfile):
            return tryfile

    return


def whence_file(py_script):
    """Do a shell-like path lookup for py_script and return the results.
    If we can't find anything return py_script"""
    if py_script.find(os.sep) != -1:
        return py_script
    for dirname in os.environ['PATH'].split(os.pathsep):
        py_script_try = os.path.join(dirname, py_script)
        if os.path.exists(py_script_try):
            return py_script_try

    return py_script


def path_expanduser_abs(filename):
    return os.path.abspath(os.path.expanduser(filename))


if __name__ == '__main__':
    import sys
    print (
     file2module(sys.argv[0]), sys.argv[0])
    ok = is_ok_line_for_breakpoint(__file__, 1, sys.stdout.write)
    print ('\nCan stop at line 1? ', ok)
    ok = is_ok_line_for_breakpoint(__file__, 2, sys.stdout.write)
    print ('\nCan stop at line 2? ', ok)
    print path_expanduser_abs('./.pydbgrrc')
    print path_expanduser_abs('~/.pydbgrrc')