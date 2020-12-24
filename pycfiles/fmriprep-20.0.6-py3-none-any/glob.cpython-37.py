# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-92t6atcz/setuptools/setuptools/glob.py
# Compiled at: 2020-04-16 14:32:20
# Size of source mod 2**32: 5084 bytes
"""
Filename globbing utility. Mostly a copy of `glob` from Python 3.5.

Changes include:
 * `yield from` and PEP3102 `*` removed.
 * Hidden files are not ignored.
"""
import os, re, fnmatch
__all__ = [
 'glob', 'iglob', 'escape']

def glob(pathname, recursive=False):
    """Return a list of paths matching a pathname pattern.

    The pattern may contain simple shell-style wildcards a la
    fnmatch. However, unlike fnmatch, filenames starting with a
    dot are special cases that are not matched by '*' and '?'
    patterns.

    If recursive is true, the pattern '**' will match any files and
    zero or more directories and subdirectories.
    """
    return list(iglob(pathname, recursive=recursive))


def iglob(pathname, recursive=False):
    """Return an iterator which yields the paths matching a pathname pattern.

    The pattern may contain simple shell-style wildcards a la
    fnmatch. However, unlike fnmatch, filenames starting with a
    dot are special cases that are not matched by '*' and '?'
    patterns.

    If recursive is true, the pattern '**' will match any files and
    zero or more directories and subdirectories.
    """
    it = _iglob(pathname, recursive)
    if recursive:
        if _isrecursive(pathname):
            s = next(it)
            assert not s
    return it


def _iglob(pathname, recursive):
    dirname, basename = os.path.split(pathname)
    if not has_magic(pathname):
        if basename:
            if os.path.lexists(pathname):
                yield pathname
        elif os.path.isdir(dirname):
            yield pathname
        return
        if not dirname:
            if recursive and _isrecursive(basename):
                for x in glob2(dirname, basename):
                    yield x

            else:
                for x in glob1(dirname, basename):
                    yield x

            return
    elif dirname != pathname:
        if has_magic(dirname):
            dirs = _iglob(dirname, recursive)
        else:
            dirs = [
             dirname]
        if has_magic(basename):
            if recursive and _isrecursive(basename):
                glob_in_dir = glob2
            else:
                glob_in_dir = glob1
    else:
        glob_in_dir = glob0
    for dirname in dirs:
        for name in glob_in_dir(dirname, basename):
            yield os.path.join(dirname, name)


def glob1(dirname, pattern):
    if not dirname:
        if isinstance(pattern, bytes):
            dirname = os.curdir.encode('ASCII')
        else:
            dirname = os.curdir
    try:
        names = os.listdir(dirname)
    except OSError:
        return []
    else:
        return fnmatch.filter(names, pattern)


def glob0(dirname, basename):
    if (basename or os.path.isdir)(dirname):
        return [
         basename]
    else:
        if os.path.lexists(os.path.join(dirname, basename)):
            return [
             basename]
    return []


def glob2(dirname, pattern):
    assert _isrecursive(pattern)
    yield pattern[:0]
    for x in _rlistdir(dirname):
        yield x


def _rlistdir(dirname):
    if not dirname:
        if isinstance(dirname, bytes):
            dirname = os.curdir.encode('ASCII')
        else:
            dirname = os.curdir
    try:
        names = os.listdir(dirname)
    except os.error:
        return
    else:
        for x in names:
            yield x
            path = os.path.join(dirname, x) if dirname else x
            for y in _rlistdir(path):
                yield os.path.join(x, y)


magic_check = re.compile('([*?[])')
magic_check_bytes = re.compile(b'([*?[])')

def has_magic(s):
    if isinstance(s, bytes):
        match = magic_check_bytes.search(s)
    else:
        match = magic_check.search(s)
    return match is not None


def _isrecursive(pattern):
    if isinstance(pattern, bytes):
        return pattern == b'**'
    return pattern == '**'


def escape(pathname):
    """Escape all special characters.
    """
    drive, pathname = os.path.splitdrive(pathname)
    if isinstance(pathname, bytes):
        pathname = magic_check_bytes.sub(b'[\\1]', pathname)
    else:
        pathname = magic_check.sub('[\\1]', pathname)
    return drive + pathname