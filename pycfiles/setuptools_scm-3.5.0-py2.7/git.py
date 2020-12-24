# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/setuptools_scm/git.py
# Compiled at: 2020-02-13 15:05:29
from .config import Configuration
from .utils import do_ex, trace, has_command
from .version import meta
from os.path import isfile, join
import warnings
try:
    from os.path import samefile
except ImportError:
    from .win_py31_compat import samefile

DEFAULT_DESCRIBE = 'git describe --dirty --tags --long --match *.*'

class GitWorkdir(object):
    """experimental, may change at any time"""

    def __init__(self, path):
        self.path = path

    def do_ex(self, cmd):
        return do_ex(cmd, cwd=self.path)

    @classmethod
    def from_potential_worktree(cls, wd):
        real_wd, _, ret = do_ex('git rev-parse --show-toplevel', wd)
        if ret:
            return
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
        warnings.warn(('"{}" is shallow and may cause errors').format(wd.path))


def fetch_on_shallow(wd):
    """experimental, may change at any time"""
    if wd.is_shallow():
        warnings.warn('"%s" was shallow, git fetch was used to rectify')
        wd.fetch_shallow()


def fail_on_shallow(wd):
    """experimental, may change at any time"""
    if wd.is_shallow():
        raise ValueError('%r is shallow, please correct with "git fetch --unshallow"' % wd.path)


def parse(root, describe_command=DEFAULT_DESCRIBE, pre_parse=warn_on_shallow, config=None):
    """
    :param pre_parse: experimental pre_parse action, may change at any time
    """
    if not config:
        config = Configuration(root=root)
    if not has_command('git'):
        return
    else:
        wd = GitWorkdir.from_potential_worktree(config.absolute_root)
        if wd is None:
            return
        if pre_parse:
            pre_parse(wd)
        if config.git_describe_command:
            describe_command = config.git_describe_command
        out, unused_err, ret = wd.do_ex(describe_command)
        if ret:
            rev_node = wd.node()
            dirty = wd.is_dirty()
            if rev_node is None:
                return meta('0.0', distance=0, dirty=dirty, config=config)
            return meta('0.0', distance=wd.count_all_nodes(), node='g' + rev_node, dirty=dirty, branch=wd.get_branch(), config=config)
        tag, number, node, dirty = _git_parse_describe(out)
        branch = wd.get_branch()
        if number:
            return meta(tag, config=config, distance=number, node=node, dirty=dirty, branch=branch)
        return meta(tag, config=config, node=node, dirty=dirty, branch=branch)
        return


def _git_parse_describe(describe_output):
    if describe_output.endswith('-dirty'):
        dirty = True
        describe_output = describe_output[:-6]
    else:
        dirty = False
    tag, number, node = describe_output.rsplit('-', 2)
    number = int(number)
    return (tag, number, node, dirty)