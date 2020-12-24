# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/david/src/python/mockfs/env27/lib/python2.7/site-packages/mockfs/__init__.py
# Compiled at: 2020-03-21 23:28:53
import os, glob, shutil
from .mfs import MockFS
from .mfs import builtins
from . import compat
from . import storage
__version__ = '1.1.1'

def replace_builtins(entries=None):
    """
    Replace builtin functions with mockfs.

    :param entries: Dictionary mapping paths to content
    :returns: Newly installed :class:`mockfs.MockFS` handler

    >>> import os
    >>> import mockfs
    >>> fs = mockfs.replace_builtins()
    >>> fs.add_entries({
    ...         '/bin/sh': 'contents',
    ...         '/bin/ls': 'contents',
    ... })
    >>> assert(os.listdir('/bin') == ['ls', 'sh'])
    >>> mockfs.restore_builtins()

    """
    mfs = MockFS()
    if entries is not None:
        mfs.add_entries(entries)
    glob.glob = mfs.glob
    os.chdir = mfs.cwd.chdir
    os.getcwd = mfs.cwd.getcwd
    os.listdir = mfs.listdir
    os.makedirs = mfs.makedirs
    os.path.abspath = mfs.abspath
    os.path.exists = mfs.exists
    os.path.getsize = mfs.getsize
    os.path.islink = mfs.islink
    os.path.isdir = mfs.isdir
    os.path.isfile = mfs.isfile
    os.remove = mfs.remove
    os.rmdir = mfs.rmdir
    os.unlink = mfs.remove
    os.walk = mfs.walk
    shutil.rmtree = mfs.rmtree
    if compat.PY2:
        os.getcwdu = mfs.cwd.getcwdu
    storage.backend = mfs.backend
    storage.replace_builtins()
    return mfs


def restore_builtins():
    """Restore the original builtin functions."""
    for k, v in builtins.items():
        mod, func = k.rsplit('.', 1)
        name_elts = mod.split('.')
        top = name_elts.pop(0)
        module = globals()[top]
        for elt in name_elts:
            module = getattr(module, elt)

        setattr(module, func, v)

    storage.restore_builtins()