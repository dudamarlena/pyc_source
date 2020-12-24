# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\david\Projects\cosmicdb\cosmicdb\__init__.py
# Compiled at: 2019-08-11 02:26:54
# Size of source mod 2**32: 129 bytes
VERSION = (0, 0, 31)

def get_version():
    """Return the version as a string."""
    return '.'.join(map(str, VERSION))