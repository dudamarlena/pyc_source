# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/clean/delete.py
# Compiled at: 2018-03-24 01:57:55
# Size of source mod 2**32: 185 bytes
__doc__ = 'Delete file move setting(s).'
from .config import Config

def delete_config(id: int):
    """Delete config by id."""
    config = Config()
    return config.delete_glob_path(id)