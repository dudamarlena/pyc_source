# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/molsen/Python/CPython-3.3.6/lib/python3.3/site-packages/pathlt/transforms.py
# Compiled at: 2016-02-26 17:06:35
# Size of source mod 2**32: 2904 bytes
from __future__ import absolute_import, division, generators, nested_scopes, print_function, unicode_literals, with_statement
import re, os, fnmatch

def parentdir_expand(path):
    """ Expand parent directory traversal

  Allow the user to specify ..<n> and expand to a recognized directory path.
  for example ..5 would expand to ../../../../..

  :param path: str
  :return: str
  """
    if path[0:2] != '..':
        return path
    else:
        parentdir_match = '\\.\\.(\\d*){0}?(.*)'.format(os.path.sep)
        matches = re.match(parentdir_match, path)
        expand_depth = matches.group(1) or 1
        extra_path = matches.group(2)
        parent_path = os.path.join(*(['..'] * int(expand_depth)))
        return os.path.join(parent_path, extra_path)


def physical_path(path, transform_callback=None):
    """ Return the physical path if path ends with //

    :param path: str
    :return: str
    """
    transform_callback = transform_callback or os.path.realpath
    if re.match('.*(?<!\\\\)//', path):
        return transform_callback(path)
    else:
        return path


def __disambiguate_path(root, path, cwd_callback=None, listdir_callback=None):
    """ Check root dir for unambiguous paths that satisfy path

    For example if root contained the following files:

    src
    tests
    test_output

    s -> src
    test -> None
    test_ -> test_output

    :param root: str
    :param path: str
    :param cwd_callback: function
    :param listdir_callback: function
    :return: str or None
    """
    cwd_callback = cwd_callback or os.getcwd
    listdir_callback = listdir_callback or os.listdir
    root = root or cwd_callback()
    try:
        candidates = [f for f in listdir_callback(root) if fnmatch.fnmatch(f, '{0}*'.format(path))]
    except OSError:
        return

    if len(candidates) == 1:
        return candidates[0]
    else:
        return
        return


def unambiguous_path(path, exists_callback=None, disambiguate_callback=None):
    """ Return a real path from an unambiguous string

    Expand each portion of the path when the string unambiguously references
    a single path.

    :param path:
    :param exists_callback: function
    :return: str or None
    """
    exists_callback = exists_callback or os.path.exists
    disambiguate_callback = disambiguate_callback or __disambiguate_path
    if exists_callback(path):
        return path
    else:
        head, tail = os.path.split(path)
        if head:
            root = unambiguous_path(head, exists_callback, disambiguate_callback)
        else:
            root = head
        tail = disambiguate_callback(root, tail)
        if tail:
            return os.path.join(root, tail)
        return path