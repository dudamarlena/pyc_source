# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/site-packages/javatools/dirutils.py
# Compiled at: 2018-10-18 16:07:18
# Size of source mod 2**32: 5709 bytes
"""
Utility module for discovering the differences between two directory
trees

:author: Christopher O'Brien  <obriencj@gmail.com>
:license: LGPL
"""
from filecmp import dircmp
from fnmatch import fnmatch
from os import makedirs, walk
from os.path import exists, isdir, join, relpath
from shutil import copy
LEFT = 'left only'
RIGHT = 'right only'
DIFF = 'changed'
SAME = 'same'
BOTH = SAME

def fnmatches(entry, *pattern_list):
    """
    returns true if entry matches any of the glob patterns, false
    otherwise
    """
    for pattern in pattern_list:
        if pattern and fnmatch(entry, pattern):
            return True

    return False


def makedirsp(dirname):
    """
    create dirname if it doesn't exist
    """
    if dirname:
        if not exists(dirname):
            makedirs(dirname)


def copydir(orig, dest):
    """
    copies directory orig to dest. Returns a list of tuples of
    relative filenames which were copied from orig to dest
    """
    copied = list()
    makedirsp(dest)
    for root, dirs, files in walk(orig):
        for d in dirs:
            makedirsp(join(dest, d))

        for f in files:
            root_f = join(root, f)
            dest_f = join(dest, relpath(root_f, orig))
            copy(root_f, dest_f)
            copied.append((root_f, dest_f))

    return copied


def compare(left, right):
    """
    generator emiting pairs indicating the contents of the left and
    right directories. The pairs are in the form of (difference,
    filename) where difference is one of the LEFT, RIGHT, DIFF, or
    BOTH constants. This generator recursively walks both trees.
    """
    dc = dircmp(left, right, ignore=[])
    return _gen_from_dircmp(dc, left, right)


def _gen_from_dircmp(dc, lpath, rpath):
    """
    do the work of comparing the dircmp
    """
    left_only = dc.left_only
    left_only.sort()
    for f in left_only:
        fp = join(dc.left, f)
        if isdir(fp):
            for r, _ds, fs in walk(fp):
                r = relpath(r, lpath)
                for f in fs:
                    yield (
                     LEFT, join(r, f))

        else:
            yield (
             LEFT, relpath(fp, lpath))

    right_only = dc.right_only
    right_only.sort()
    for f in right_only:
        fp = join(dc.right, f)
        if isdir(fp):
            for r, _ds, fs in walk(fp):
                r = relpath(r, rpath)
                for f in fs:
                    yield (
                     RIGHT, join(r, f))

        else:
            yield (
             RIGHT, relpath(fp, rpath))

    diff_files = dc.diff_files
    diff_files.sort()
    for f in diff_files:
        yield (DIFF, join(relpath(dc.right, rpath), f))

    same_files = dc.same_files
    same_files.sort()
    for f in same_files:
        yield (BOTH, join(relpath(dc.left, lpath), f))

    subdirs = dc.subdirs.values()
    subdirs = sorted(subdirs)
    for sub in subdirs:
        for event in _gen_from_dircmp(sub, lpath, rpath):
            yield event


def collect_compare(left, right):
    """
    returns a tuple of four lists describing the file paths that have
    been (in order) added, removed, altered, or left the same
    """
    return collect_compare_into(left, right, [], [], [], [])


def collect_compare_into(left, right, added, removed, altered, same):
    """
    collect the results of compare into the given lists (or None if
    you do not wish to collect results of that type. Returns a tuple
    of (added, removed, altered, same)
    """
    for event, filename in compare(left, right):
        if event == LEFT:
            group = removed
        else:
            if event == RIGHT:
                group = added
            else:
                if event == DIFF:
                    group = altered
                else:
                    if event == BOTH:
                        group = same
                    else:
                        assert False
        if group is not None:
            group.append(filename)

    return (
     added, removed, altered, same)


class ClosingContext(object):
    __doc__ = '\n    A simple context manager which is created with an object instance,\n    and will return that instance from __enter__ and call the close\n    method on the instance in __exit__\n    '

    def __init__(self, managed):
        self.managed = managed

    def __enter__(self):
        return self.managed

    def __exit__(self, exc_type, _exc_val, _exc_tb):
        managed = self.managed
        self.managed = None
        if managed is not None:
            if hasattr(managed, 'close'):
                managed.close()
        return exc_type is None


def closing(managed):
    """
    If the managed object already provides its own context management
    via the __enter__ and __exit__ methods, it is returned
    unchanged. However, if the instance does not, a ClosingContext
    will be created to wrap it. When the ClosingContext exits, it will
    call managed.close()
    """
    if managed is None or hasattr(managed, '__enter__'):
        return managed
    return ClosingContext(managed)