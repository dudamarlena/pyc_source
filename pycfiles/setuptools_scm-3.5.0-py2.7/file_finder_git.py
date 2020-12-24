# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/setuptools_scm/file_finder_git.py
# Compiled at: 2020-02-13 15:05:29
import os, subprocess, tarfile, logging
from .file_finder import scm_find_files
from .utils import trace
log = logging.getLogger(__name__)

def _git_toplevel(path):
    try:
        with open(os.devnull, 'wb') as (devnull):
            out = subprocess.check_output([
             'git', 'rev-parse', '--show-toplevel'], cwd=path or '.', universal_newlines=True, stderr=devnull)
        trace('find files toplevel', out)
        return os.path.normcase(os.path.realpath(out.strip()))
    except subprocess.CalledProcessError:
        return
    except OSError:
        return

    return


def _git_interpret_archive(fd, toplevel):
    with tarfile.open(fileobj=fd, mode='r|*') as (tf):
        git_files = set()
        git_dirs = {toplevel}
        for member in tf.getmembers():
            name = os.path.normcase(member.name).replace('/', os.path.sep)
            if member.type == tarfile.DIRTYPE:
                git_dirs.add(name)
            else:
                git_files.add(name)

        return (
         git_files, git_dirs)


def _git_ls_files_and_dirs(toplevel):
    cmd = [
     'git', 'archive', '--prefix', toplevel + os.path.sep, 'HEAD']
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, cwd=toplevel)
    try:
        try:
            return _git_interpret_archive(proc.stdout, toplevel)
        finally:
            proc.stdout.close()
            proc.terminate()

    except Exception:
        if proc.wait() != 0:
            log.exception("listing git files failed - pretending there aren't any")
        return (
         (), ())


def git_find_files(path=''):
    toplevel = _git_toplevel(path)
    if not toplevel:
        return []
    git_files, git_dirs = _git_ls_files_and_dirs(toplevel)
    return scm_find_files(path, git_files, git_dirs)