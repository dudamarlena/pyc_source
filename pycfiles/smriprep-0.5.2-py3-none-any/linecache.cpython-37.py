# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/src/smriprep/build/lib/python3.7/linecache.py
# Compiled at: 2019-09-12 11:41:56
# Size of source mod 2**32: 5312 bytes
"""Cache lines from Python source files.

This is intended to read lines from modules imported -- hence if a filename
is not found, it will look down the module search path for a file by
that name.
"""
import functools, sys, os, tokenize
__all__ = [
 'getline', 'clearcache', 'checkcache']

def getline(filename, lineno, module_globals=None):
    lines = getlines(filename, module_globals)
    if 1 <= lineno <= len(lines):
        return lines[(lineno - 1)]
    return ''


cache = {}

def clearcache():
    """Clear the cache entirely."""
    global cache
    cache = {}


def getlines(filename, module_globals=None):
    """Get the lines for a Python source file from the cache.
    Update the cache if it doesn't contain an entry for this file already."""
    if filename in cache:
        entry = cache[filename]
        if len(entry) != 1:
            return cache[filename][2]
    try:
        return updatecache(filename, module_globals)
    except MemoryError:
        clearcache()
        return []


def checkcache(filename=None):
    """Discard cache entries that are out of date.
    (This is not checked upon each call!)"""
    if filename is None:
        filenames = list(cache.keys())
    else:
        if filename in cache:
            filenames = [
             filename]
        else:
            return
    for filename in filenames:
        entry = cache[filename]
        if len(entry) == 1:
            continue
        size, mtime, lines, fullname = entry
        if mtime is None:
            continue
        try:
            stat = os.stat(fullname)
        except OSError:
            del cache[filename]
            continue

        if size != stat.st_size or mtime != stat.st_mtime:
            del cache[filename]


def updatecache(filename, module_globals=None):
    """Update a cache entry and return its list of lines.
    If something's wrong, print a message, discard the cache entry,
    and return an empty list."""
    if filename in cache:
        if len(cache[filename]) != 1:
            del cache[filename]
    elif filename:
        if filename.startswith('<'):
            if filename.endswith('>'):
                return []
    else:
        fullname = filename
        try:
            stat = os.stat(fullname)
        except OSError:
            basename = filename
            if lazycache(filename, module_globals):
                try:
                    data = cache[filename][0]()
                except (ImportError, OSError):
                    pass
                else:
                    if data is None:
                        return []
                    cache[filename] = (
                     len(data), None,
                     [line + '\n' for line in data.splitlines()], fullname)
                    return cache[filename][2]
            if os.path.isabs(filename):
                return []
            for dirname in sys.path:
                try:
                    fullname = os.path.join(dirname, basename)
                except (TypeError, AttributeError):
                    continue

                try:
                    stat = os.stat(fullname)
                    break
                except OSError:
                    pass

            else:
                return []

    try:
        with tokenize.open(fullname) as (fp):
            lines = fp.readlines()
    except OSError:
        return []
    else:
        if lines:
            if not lines[(-1)].endswith('\n'):
                lines[(-1)] += '\n'
        size, mtime = stat.st_size, stat.st_mtime
        cache[filename] = (size, mtime, lines, fullname)
        return lines


def lazycache(filename, module_globals):
    """Seed the cache for filename with module_globals.

    The module loader will be asked for the source only when getlines is
    called, not immediately.

    If there is an entry in the cache already, it is not altered.

    :return: True if a lazy load is registered in the cache,
        otherwise False. To register such a load a module loader with a
        get_source method must be found, the filename must be a cachable
        filename, and the filename must not be already cached.
    """
    if filename in cache:
        if len(cache[filename]) == 1:
            return True
        return False
        if filename:
            if filename.startswith('<'):
                if filename.endswith('>'):
                    return False
    elif module_globals:
        if '__loader__' in module_globals:
            name = module_globals.get('__name__')
            loader = module_globals['__loader__']
            get_source = getattr(loader, 'get_source', None)
            if name:
                if get_source:
                    get_lines = functools.partial(get_source, name)
                    cache[filename] = (get_lines,)
                    return True
    return False