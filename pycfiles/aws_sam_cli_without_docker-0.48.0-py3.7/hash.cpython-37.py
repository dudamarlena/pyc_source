# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/lib/utils/hash.py
# Compiled at: 2020-03-21 12:32:11
# Size of source mod 2**32: 1689 bytes
"""
Hash calculation utilities for files and directories.
"""
import os, hashlib
BLOCK_SIZE = 4096

def file_checksum(file_name):
    """

    Parameters
    ----------
    file_name: file name of the file for which md5 checksum is required.

    Returns
    -------
    md5 checksum of the given file.

    """
    with open(file_name, 'rb') as (file_handle):
        md5 = hashlib.md5()
        curpos = file_handle.tell()
        file_handle.seek(0)
        buf = file_handle.read(BLOCK_SIZE)
        while buf:
            md5.update(buf)
            buf = file_handle.read(BLOCK_SIZE)

        file_handle.seek(curpos)
        return md5.hexdigest()


def dir_checksum(directory, followlinks=True):
    """

    Parameters
    ----------
    directory : A directory with an absolute path
    followlinks: Follow symbolic links through the given directory

    Returns
    -------
    md5 checksum of the directory.

    """
    md5_dir = hashlib.md5()
    for dirpath, _, filenames in os.walk(directory, followlinks=followlinks):
        for filepath in [os.path.join(dirpath, filename) for filename in filenames]:
            md5_dir.update(filepath.encode('utf-8'))
            filepath_checksum = file_checksum(filepath)
            md5_dir.update(filepath_checksum.encode('utf-8'))

    return md5_dir.hexdigest()