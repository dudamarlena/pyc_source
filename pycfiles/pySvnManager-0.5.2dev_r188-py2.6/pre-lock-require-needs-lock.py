# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysvnmanager/hooks/init/hook1.5/scripts/pre-lock-require-needs-lock.py
# Compiled at: 2010-09-24 12:39:25
import sys, os, os.path
from svn import repos, fs, core

def main(pool, repos_dir, path):
    fs_ptr = repos.svn_repos_fs(repos.svn_repos_open(repos_dir, pool))
    youngest_rev = fs.svn_fs_youngest_rev(fs_ptr, pool)
    root = fs.svn_fs_revision_root(fs_ptr, youngest_rev, pool)
    if not fs.svn_fs_node_prop(root, path, core.SVN_PROP_NEEDS_LOCK, pool):
        sys.stderr.write("Locking of path '%s' prohibited by repository policy (must have\n%s property set)\n" % (path, core.SVN_PROP_NEEDS_LOCK))
        return 1
    return 0


def _usage_and_exit():
    sys.stderr.write('\nUsage: %s REPOS-DIR PATH\n\nThis script, intended for use as a Subversion pre-lock hook, verifies that\nthe PATH that USER is attempting to lock has the %s property\nset on it, returning success iff it does.\n' % (os.path.basename(sys.argv[0]), core.SVN_PROP_NEEDS_LOCK))
    sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        _usage_and_exit()
    sys.exit(core.run_app(main, sys.argv[1], sys.argv[2]))