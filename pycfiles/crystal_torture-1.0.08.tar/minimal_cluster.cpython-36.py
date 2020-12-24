# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cor/bin/src/crystal_torture/crystal_torture/minimal_cluster.py
# Compiled at: 2019-04-30 02:12:29
# Size of source mod 2**32: 593 bytes


class minimal_Cluster:
    __doc__ = '\n    minimal_Cluster class: minimal cluster object for returning tortuosity data from graph\n    '

    def __init__(self, site_indices, size):
        """
        Initialise a minimal cluster.

        Args:
            - site_indices ((int)): set of site indices in the cluster.
            - periodicity (int): degree of periodicity in cluster
            - tortuosity (real): average tortuosity of cluster
            
        """
        self.site_indices = site_indices
        self.periodic = None
        self.tortuosity = None
        self.size = size