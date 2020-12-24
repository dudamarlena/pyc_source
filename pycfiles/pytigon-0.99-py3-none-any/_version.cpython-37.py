# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-76h68wr6/tqdm/tqdm/_version.py
# Compiled at: 2020-04-19 04:11:09
# Size of source mod 2**32: 2318 bytes
import os
from io import open as io_open
__all__ = [
 '__version__']
version_info = (4, 45, 0)
__version__ = '.'.join(map(str, version_info))
scriptdir = os.path.dirname(__file__)
gitdir = os.path.abspath(os.path.join(scriptdir, '..', '.git'))
if os.path.isdir(gitdir):
    extra = None
    with io_open(os.path.join(gitdir, 'config'), 'r') as (fh_config):
        if 'tqdm' in fh_config.read():
            with io_open(os.path.join(gitdir, 'HEAD'), 'r') as (fh_head):
                extra = fh_head.readline().strip()
            if 'ref:' in extra:
                ref_file = extra[5:]
                branch_name = ref_file.rsplit('/', 1)[(-1)]
                ref_file_path = os.path.abspath(os.path.join(gitdir, ref_file))
                if os.path.relpath(ref_file_path, gitdir).replace('\\', '/') != ref_file:
                    extra = None
                else:
                    with io_open(ref_file_path, 'r') as (fh_branch):
                        commit_hash = fh_branch.readline().strip()
                        extra = commit_hash[:8]
                        if branch_name != 'master':
                            extra += '.' + branch_name
            else:
                extra = extra[:8]
    if extra is not None:
        try:
            with io_open(os.path.join(gitdir, 'refs', 'tags', 'v' + __version__)) as (fdv):
                if fdv.readline().strip()[:8] != extra[:8]:
                    __version__ += '-' + extra
        except Exception as e:
            try:
                if 'No such file' not in str(e):
                    raise
            finally:
                e = None
                del e