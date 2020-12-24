# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/ocfl/disposition.py
# Compiled at: 2018-10-30 09:14:14
# Size of source mod 2**32: 651 bytes
"""Handle different storage dispositions."""
from .identity import Identity
from .ntree import Ntree
from .uuid_quadtree import UUIDQuadtree

def get_dispositor(disposition=None):
    """Find Dispositor object for the given disposition."""
    if disposition == 'pairtree':
        return Ntree(n=2)
    else:
        if disposition == 'tripletree':
            return Ntree(n=3)
        else:
            if disposition == 'quadtree':
                return Ntree(n=4)
            if disposition == 'uuid_quadtree':
                return UUIDQuadtree()
        if disposition == 'identity':
            return Identity()
    raise Exception('Unsupported disposition %s, aborting!' % disposition)