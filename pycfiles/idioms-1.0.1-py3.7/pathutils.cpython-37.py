# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/idioms/utils/pathutils.py
# Compiled at: 2019-05-09 14:20:58
# Size of source mod 2**32: 222 bytes
import os

def realpath(filepath):
    """Return the real path corresponding to the given filepath, expanding any tildes and resolving symlinks."""
    return os.path.realpath(os.path.abspath(os.path.expanduser(filepath)))