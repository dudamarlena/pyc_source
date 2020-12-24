# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysvnmanager/hooks/init/hook1.5/scripts/pre-commit-check.py
# Compiled at: 2010-09-24 12:39:25
import sys, os, os.path
from svn import repos, fs, delta, core

def test_props(props):
    """Validate the PROPS (a dictionary mapping property names to
  values) set on the transaction.  Return 0 if all is well, non-zero
  otherwise."""
    return 0


def test_path_change(path, change):
    """Validate the CHANGE made to PATH in the transaction.  Return 0
  if all is well, non-zero otherwise."""
    item_kind = change.item_kind
    prop_changes = change.prop_changes
    text_changed = change.text_changed
    base_path = change.base_path
    base_rev = change.base_rev
    added = change.added
    return 1


def main(pool, repos_dir, txn):
    fs_ptr = repos.svn_repos_fs(repos.svn_repos_open(repos_dir, pool))
    root = fs.txn_root(fs.open_txn(fs_ptr, txn, pool), pool)
    cc = repos.ChangeCollector(fs_ptr, root, pool)
    retval = test_props(cc.get_root_props())
    if retval:
        return retval
    (e_ptr, e_baton) = delta.make_editor(cc, pool)
    repos.svn_repos_replay(root, e_ptr, e_baton, pool)
    changes = cc.get_changes()
    paths = changes.keys()
    paths.sort(lambda a, b: core.svn_path_compare_paths(a, b))
    for path in paths:
        change = changes[path]
        retval = test_path_change(path, change)
        if retval:
            return retval

    return 0


def _usage_and_exit():
    sys.stderr.write('USAGE: %s REPOS-DIR TXN-NAME\n' % sys.argv[0])
    sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        _usage_and_exit()
    sys.exit(core.run_app(main, sys.argv[1], sys.argv[2]))