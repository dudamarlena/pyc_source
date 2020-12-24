# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/mvc/support/file_utils.py
# Compiled at: 2020-03-07 03:51:49
# Size of source mod 2**32: 2917 bytes
import os

def get_case_insensitive_glob(*strings):
    """Ex: '*.ora' => '*.[oO][rR][aA]' """
    return ['*.%s' % ''.join(['[%s%s]' % (c.lower(), c.upper()) for c in string.split('.')[1]]) for string in strings]


def retrieve_lowercase_extension(glob):
    """Ex: '*.[oO][rR][aA]' => '*.ora' """
    return ''.join([c.replace('[', '').replace(']', '')[:-1] for c in glob.split('][')])


def __posix_relpath(path, start=os.curdir):
    """Return a relative version of a path"""
    if not path:
        raise ValueError('no path specified')
    start_list = os.path.abspath(start).split(os.sep)
    path_list = os.path.abspath(path).split(os.sep)
    i = len(os.path.commonprefix([start_list, path_list]))
    rel_list = [
     os.pardir] * (len(start_list) - i) + path_list[i:]
    if not rel_list:
        return os.curdir
    else:
        return (os.path.join)(*rel_list)


def __nt_relpath(path, start=os.curdir):
    """Return a relative version of a path"""
    if not path:
        raise ValueError('no path specified')
    start_list = os.path.abspath(start).split(os.sep)
    path_list = os.path.abspath(path).split(os.sep)
    if start_list[0].lower() != path_list[0].lower():
        unc_path, rest = os.path.splitunc(path)
        unc_start, rest = os.path.splitunc(start)
        if bool(unc_path) ^ bool(unc_start):
            raise ValueError('Cannot mix UNC and non-UNC paths (%s and %s)' % (
             path, start))
        else:
            raise ValueError('path is on drive %s, start on drive %s' % (
             path_list[0], start_list[0]))
        for i in range(min(len(start_list), len(path_list))):
            if start_list[i].lower() != path_list[i].lower():
                break
            else:
                i += 1

        rel_list = [os.pardir] * (len(start_list) - i) + path_list[i:]
        return rel_list or os.curdir
    else:
        return (os.path.join)(*rel_list)


try:
    import os.path.relpath
    relpath = os.path.relpath
except ImportError:
    if os.name == 'nt':
        relpath = __nt_relpath
    else:
        relpath = __posix_relpath