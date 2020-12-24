# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysvnmanager/hooks/init/hook1.5/scripts/check-case-insensitive.py
# Compiled at: 2010-09-24 12:39:25
import sys, locale
sys.path.append('/usr/local/subversion/lib/svn-python')
from svn import repos, fs
locale.setlocale(locale.LC_ALL, 'zh_CN.UTF8')

def canonicalize(path):
    return path.decode('utf-8').lower().encode('utf-8')


def get_new_paths(txn_root):
    new_paths = []
    for (path, change) in fs.paths_changed(txn_root).iteritems():
        if change.change_kind == fs.path_change_add or change.change_kind == fs.path_change_replace:
            new_paths.append(path)

    return new_paths


def split_path(path):
    slash = path.rindex('/')
    if slash == 0:
        return ('/', path[1:])
    return (
     path[:slash], path[slash + 1:])


def join_path(dir, name):
    if dir == '/':
        return '/' + name
    return dir + '/' + name


def ensure_names(path, names, txn_root):
    if not names.has_key(path):
        names[path] = []
        for (name, dirent) in fs.dir_entries(txn_root, path).iteritems():
            names[path].append([canonicalize(name), name])


names = {}
clashes = {}
native = locale.getlocale()[1]
if not native:
    native = 'utf-8'
repos_handle = repos.open(sys.argv[1].decode(native).encode('utf-8'))
fs_handle = repos.fs(repos_handle)
txn_handle = fs.open_txn(fs_handle, sys.argv[2].decode(native).encode('utf-8'))
txn_root = fs.txn_root(txn_handle)
new_paths = get_new_paths(txn_root)
for path in new_paths:
    (dir, name) = split_path(path)
    canonical = canonicalize(name)
    ensure_names(dir, names, txn_root)
    for name_pair in names[dir]:
        if name_pair[0] == canonical and name_pair[1] != name:
            canonical_path = join_path(dir, canonical)
            if not clashes.has_key(canonical_path):
                clashes[canonical_path] = {}
            clashes[canonical_path][join_path(dir, name)] = True
            clashes[canonical_path][join_path(dir, name_pair[1])] = True

if clashes:
    for canonical_path in clashes.iterkeys():
        sys.stderr.write(('Clash:').encode(native))
        for path in clashes[canonical_path].iterkeys():
            sys.stderr.write((" '").encode(native) + str(path).decode('utf-8').encode(native, 'replace') + ("'").encode(native))

        sys.stderr.write(('\n').encode(native))

    sys.exit(1)