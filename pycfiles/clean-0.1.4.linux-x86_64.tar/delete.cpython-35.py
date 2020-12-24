# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/clean/delete.py
# Compiled at: 2018-03-24 01:57:55
# Size of source mod 2**32: 185 bytes
"""Delete file move setting(s)."""
from .config import Config

def delete_config(id: int):
    """Delete config by id."""
    config = Config()
    return config.delete_glob_path(id)