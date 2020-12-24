# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/setuptools_scm/file_finder.py
# Compiled at: 2020-02-13 15:05:29
import os

def scm_find_files(path, scm_files, scm_dirs):
    """ setuptools compatible file finder that follows symlinks

    - path: the root directory from which to search
    - scm_files: set of scm controlled files and symlinks
      (including symlinks to directories)
    - scm_dirs: set of scm controlled directories
      (including directories containing no scm controlled files)

    scm_files and scm_dirs must be absolute with symlinks resolved (realpath),
    with normalized case (normcase)

    Spec here: http://setuptools.readthedocs.io/en/latest/setuptools.html#        adding-support-for-revision-control-systems
    """
    realpath = os.path.normcase(os.path.realpath(path))
    seen = set()
    res = []
    for dirpath, dirnames, filenames in os.walk(realpath, followlinks=True):
        realdirpath = os.path.normcase(os.path.realpath(dirpath))

        def _link_not_in_scm(n):
            fn = os.path.join(realdirpath, os.path.normcase(n))
            return os.path.islink(fn) and fn not in scm_files

        if realdirpath not in scm_dirs:
            dirnames[:] = []
            continue
        if os.path.islink(dirpath) and not os.path.relpath(realdirpath, realpath).startswith(os.pardir):
            res.append(os.path.join(path, os.path.relpath(dirpath, path)))
            dirnames[:] = []
            continue
        if realdirpath in seen:
            dirnames[:] = []
            continue
        dirnames[:] = [ dn for dn in dirnames if not _link_not_in_scm(dn) ]
        for filename in filenames:
            if _link_not_in_scm(filename):
                continue
            fullfilename = os.path.join(dirpath, filename)
            if os.path.normcase(os.path.realpath(fullfilename)) in scm_files:
                res.append(os.path.join(path, os.path.relpath(fullfilename, path)))

        seen.add(realdirpath)

    return res