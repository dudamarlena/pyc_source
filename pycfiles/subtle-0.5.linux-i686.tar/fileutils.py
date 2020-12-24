# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/guessit/fileutils.py
# Compiled at: 2013-03-18 16:30:48
from __future__ import unicode_literals
from guessit import s, u
import os.path, zipfile

def split_path(path):
    r"""Splits the given path into the list of folders and the filename (or the
    last folder if you gave it a folder path.

    If the given path was an absolute path, the first element will always be:
     - the '/' root folder on Unix systems
     - the drive letter on Windows systems (eg: r'C:\')
     - the mount point '\\' on Windows systems (eg: r'\\host\share')

    >>> s(split_path('/usr/bin/smewt'))
    ['/', 'usr', 'bin', 'smewt']

    >>> s(split_path('relative_path/to/my_folder/'))
    ['relative_path', 'to', 'my_folder']

    """
    result = []
    while True:
        head, tail = os.path.split(path)
        if head == b'/' and tail == b'':
            return [b'/'] + result
        if (len(head) == 3 and head[1:] == b':\\' or len(head) == 2 and head == b'\\\\') and tail == b'':
            return [head] + result
        if head == b'' and tail == b'':
            return result
        if not tail:
            path = head
            continue
        result = [tail] + result
        path = head


def file_in_same_dir(ref_file, desired_file):
    """Return the path for a file in the same dir as a given reference file.

    >>> s(file_in_same_dir('~/smewt/smewt.db', 'smewt.settings'))
    '~/smewt/smewt.settings'

    """
    return os.path.join(*(split_path(ref_file)[:-1] + [desired_file]))


def load_file_in_same_dir(ref_file, filename):
    """Load a given file. Works even when the file is contained inside a zip."""
    path = split_path(ref_file)[:-1] + [filename]
    for i, p in enumerate(path):
        if p.endswith(b'.zip'):
            zfilename = os.path.join(*path[:i + 1])
            zfile = zipfile.ZipFile(zfilename)
            return zfile.read((b'/').join(path[i + 1:]))

    return u(open(os.path.join(*path)).read())