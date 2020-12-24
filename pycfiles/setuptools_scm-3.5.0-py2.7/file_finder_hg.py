# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/setuptools_scm/file_finder_hg.py
# Compiled at: 2020-02-13 15:05:29
import os, subprocess
from .file_finder import scm_find_files

def _hg_toplevel(path):
    try:
        with open(os.devnull, 'wb') as (devnull):
            out = subprocess.check_output([
             'hg', 'root'], cwd=path or '.', universal_newlines=True, stderr=devnull)
        return os.path.normcase(os.path.realpath(out.strip()))
    except subprocess.CalledProcessError:
        return
    except OSError:
        return

    return


def _hg_ls_files_and_dirs(toplevel):
    hg_files = set()
    hg_dirs = {toplevel}
    out = subprocess.check_output([
     'hg', 'files'], cwd=toplevel, universal_newlines=True)
    for name in out.splitlines():
        name = os.path.normcase(name).replace('/', os.path.sep)
        fullname = os.path.join(toplevel, name)
        hg_files.add(fullname)
        dirname = os.path.dirname(fullname)
        while len(dirname) > len(toplevel) and dirname not in hg_dirs:
            hg_dirs.add(dirname)
            dirname = os.path.dirname(dirname)

    return (
     hg_files, hg_dirs)


def hg_find_files(path=''):
    toplevel = _hg_toplevel(path)
    if not toplevel:
        return []
    hg_files, hg_dirs = _hg_ls_files_and_dirs(toplevel)
    return scm_find_files(path, hg_files, hg_dirs)