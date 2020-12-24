# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\derek_2\Google Drive\nvda-addon-exploded\notepad++\scons-local-2.5.0\SCons\Scanner\Dir.py
# Compiled at: 2016-07-07 03:21:36
__revision__ = 'src/engine/SCons/Scanner/Dir.py rel_2.5.0:3543:937e55cd78f7 2016/04/09 11:29:54 bdbaddog'
import SCons.Node.FS, SCons.Scanner

def only_dirs(nodes):
    is_Dir = lambda n: isinstance(n.disambiguate(), SCons.Node.FS.Dir)
    return list(filter(is_Dir, nodes))


def DirScanner(**kw):
    """Return a prototype Scanner instance for scanning
    directories for on-disk files"""
    kw['node_factory'] = SCons.Node.FS.Entry
    kw['recursive'] = only_dirs
    return SCons.Scanner.Base(scan_on_disk, 'DirScanner', **kw)


def DirEntryScanner(**kw):
    """Return a prototype Scanner instance for "scanning"
    directory Nodes for their in-memory entries"""
    kw['node_factory'] = SCons.Node.FS.Entry
    kw['recursive'] = None
    return SCons.Scanner.Base(scan_in_memory, 'DirEntryScanner', **kw)


skip_entry = {}
skip_entry_list = [
 '.',
 '..',
 '.sconsign',
 '.sconsign.dblite',
 '.sconsign.dir',
 '.sconsign.pag',
 '.sconsign.dat',
 '.sconsign.bak',
 '.sconsign.db']
for skip in skip_entry_list:
    skip_entry[skip] = 1
    skip_entry[SCons.Node.FS._my_normcase(skip)] = 1

do_not_scan = lambda k: k not in skip_entry

def scan_on_disk(node, env, path=()):
    """
    Scans a directory for on-disk files and directories therein.

    Looking up the entries will add these to the in-memory Node tree
    representation of the file system, so all we have to do is just
    that and then call the in-memory scanning function.
    """
    try:
        flist = node.fs.listdir(node.get_abspath())
    except (IOError, OSError):
        return []

    e = node.Entry
    for f in filter(do_not_scan, flist):
        e('./' + f)

    return scan_in_memory(node, env, path)


def scan_in_memory(node, env, path=()):
    """
    "Scans" a Node.FS.Dir for its in-memory entries.
    """
    try:
        entries = node.entries
    except AttributeError:
        return []

    entry_list = sorted(filter(do_not_scan, list(entries.keys())))
    return [ entries[n] for n in entry_list ]