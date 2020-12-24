# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Users\david\Projects\cosmicdbsemantic\cosmicdb\__init__.py
# Compiled at: 2019-07-27 09:52:13
# Size of source mod 2**32: 129 bytes
VERSION = (0, 0, 37)

def get_version():
    """Return the version as a string."""
    return '.'.join(map(str, VERSION))