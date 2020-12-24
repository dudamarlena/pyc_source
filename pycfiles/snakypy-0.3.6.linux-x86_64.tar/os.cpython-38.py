# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/wc4nin/.cache/pypoetry/virtualenvs/snakypy-Jn9yRLD4-py3.8/lib/python3.8/site-packages/snakypy/utils/os.py
# Compiled at: 2020-03-21 13:29:34
# Size of source mod 2**32: 567 bytes
import os

def rmdir_blank(path):
    """Removes folders recursively if they are empty from a
    certain path."""
    for r, d, f in os.walk(path, topdown=False):
        for folder in d:
            if len(os.listdir(os.path.join(r, folder))) == 0:
                try:
                    os.rmdir(os.path.join(r, folder))
                except PermissionError:
                    raise PermissionError('No permission to remove empty folders')
                except Exception:
                    raise Exception('It was not possible to clean empty folders.')