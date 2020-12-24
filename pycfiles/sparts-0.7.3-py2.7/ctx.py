# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sparts/ctx.py
# Compiled at: 2014-04-17 23:01:18
"""Module containing various helpful context managers."""
from __future__ import absolute_import
from contextlib import contextmanager
from sparts.fileutils import NamedTemporaryDirectory
import copy, os.path, sys

@contextmanager
def tmpdir(*args, **kwargs):
    """Create a NamedTemporaryDirectory "as" the str path"""
    with NamedTemporaryDirectory() as (d):
        yield d.name


@contextmanager
def add_path(path, index=None):
    """Temporarily add `path` to the PYTHONPATH. Not thread-safe.
    
    If `index` is None, append to the end, otherwise, use `index` as specified
    to `list.insert()`"""
    if index is None:
        sys.path.append(path)
    else:
        sys.path.insert(index, path)
    try:
        yield path
    finally:
        sys.path.remove(path)

    return


@contextmanager
def chdir(path):
    """Temporarily chdir to `path`.  Not thread-safe."""
    assert os.path.exists(path)
    assert os.path.isdir(path)
    old_path = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old_path)


@contextmanager
def module_snapshot():
    """Removes any new modules from the module cache after context exit"""
    try:
        modules = copy.copy(sys.modules)
        yield
    finally:
        to_delete = [ k for k in sys.modules if k not in modules ]
        for k in to_delete:
            del sys.modules[k]