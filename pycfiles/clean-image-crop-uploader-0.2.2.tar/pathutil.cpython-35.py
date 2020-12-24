# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/clean/pathutil.py
# Compiled at: 2018-03-25 09:47:47
# Size of source mod 2**32: 374 bytes
__doc__ = 'Path utility functions.'
from os import utime
from pathlib import Path

def rm_recursive(path: Path):
    """Delete directory or file recursive."""
    if path.exists():
        if path.is_file():
            path.unlink()
            return
        if path.is_dir():
            for file in path.glob('*'):
                rm_recursive(file)

            path.rmdir()