# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\david\Projects\cosmicdbsemantic\cosmicdb\__init__.py
# Compiled at: 2019-07-27 09:52:13
# Size of source mod 2**32: 129 bytes
VERSION = (0, 0, 37)

def get_version():
    """Return the version as a string."""
    return '.'.join(map(str, VERSION))