# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fatfrog/Documents/backmap/.eggs/setuptools_scm-2.0.0-py3.6.egg/setuptools_scm/git.py
# Compiled at: 2018-04-13 13:17:12
# Size of source mod 2**32: 3798 bytes
from .utils import do_ex, trace, has_command
from .version import meta
from os.path import isfile, join
import subprocess, tarfile, warnings
try:
    from os.path import samefile
except ImportError:
    from .win_py31_compat import samefile

DEFAULT_DESCRIBE = 'git describe --dirty --tags --long --match *.*'

class GitWorkdir(object):
    __doc__ = 'experimental, may change at any time'

    def __init__(self, path):
        self.path = path

    def do_ex(self, cmd):
        return do_ex(cmd, cwd=(self.path))

    @classmethod
    def from_potential_worktree(cls, wd):
        real_wd, _, ret = do_ex('git rev-parse --show-toplevel', wd)
        if ret:
            return
        else:
            trace('real root', real_wd)
            if not samefile(real_wd, wd):
                return
            return cls(real_wd)

    def is_dirty(self):
        out, _, _ = self.do_ex('git status --porcelain --untracked-files=no')
        return bool(out)

    def get_branch(self):
        branch, err, ret = self.do_ex('git rev-parse --abbrev-ref HEAD')
        if ret:
            trace('branch err', branch, err, ret)
            return
        else:
            return branch

    def is_shallow(self):
        return isfile(join(self.path, '.git/shallow'))

    def fetch_shallow(self):
        self.do_ex('git fetch --unshallow')

    def node(self):
        rev_node, _, ret = self.do_ex('git rev-parse --verify --quiet HEAD')
        if not ret:
            return rev_node[:7]

    def count_all_nodes(self):
        revs, _, _ = self.do_ex('git rev-list HEAD')
        return revs.count('\n') + 1


def warn_on_shallow(wd):
    """experimental, may change at any time"""
    if wd.is_shallow():
        warnings.warn('"%s" is shallow and may cause errors' % (wd.path,))


def fetch_on_shallow(wd):
    """experimental, may change at any time"""
    if wd.is_shallow():
        warnings.warn('"%s" was shallow, git fetch was used to rectify')
        wd.fetch_shallow()


def fail_on_shallow(wd):
    """experimental, may change at any time"""
    if wd.is_shallow():
        raise ValueError('%r is shallow, please correct with "git fetch --unshallow"' % wd.path)


def parse(root, describe_command=DEFAULT_DESCRIBE, pre_parse=warn_on_shallow):
    """
    :param pre_parse: experimental pre_parse action, may change at any time
    """
    if not has_command('git'):
        return
    else:
        wd = GitWorkdir.from_potential_worktree(root)
        if wd is None:
            return
        if pre_parse:
            pre_parse(wd)
        out, err, ret = wd.do_ex(describe_command)
        if ret:
            rev_node = wd.node()
            dirty = wd.is_dirty()
            if rev_node is None:
                return meta('0.0', distance=0, dirty=dirty)
            else:
                return meta('0.0',
                  distance=(wd.count_all_nodes()),
                  node=('g' + rev_node),
                  dirty=dirty,
                  branch=(wd.get_branch()))
        if out.endswith('-dirty'):
            dirty = True
            out = out[:-6]
        else:
            dirty = False
        tag, number, node = out.rsplit('-', 2)
        number = int(number)
        branch = wd.get_branch()
        if number:
            return meta(tag, distance=number, node=node, dirty=dirty, branch=branch)
        return meta(tag, node=node, dirty=dirty, branch=branch)


def list_files_in_archive(path):
    """List the files that 'git archive' generates.
    """
    cmd = [
     'git', 'archive', 'HEAD']
    proc = subprocess.Popen(cmd, stdout=(subprocess.PIPE), cwd=path)
    tf = tarfile.open(fileobj=(proc.stdout), mode='r|*')
    return [member.name for member in tf.getmembers() if member.type != tarfile.DIRTYPE]