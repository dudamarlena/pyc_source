# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dan/Documents/repos/parsely/fluster/fluster/exceptions.py
# Compiled at: 2016-01-05 13:47:17
# Size of source mod 2**32: 106 bytes


class ClusterEmptyError(Exception):
    __doc__ = 'Happens when the cluster has no available clients.'