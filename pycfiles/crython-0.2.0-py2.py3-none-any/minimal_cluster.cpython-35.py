# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/cor/bin/src/crystal_torture/crystal_torture/minimal_cluster.py
# Compiled at: 2018-05-30 10:29:45
# Size of source mod 2**32: 790 bytes


class minimal_Cluster:
    """minimal_Cluster"""

    def __init__(self, site_indices, size):
        """
        Initialise a cluster.

        Args:
            site_indices ((int)): set of site indices in the cluster.
            periodicity (int): degree of periodicity in cluster
            tortuosity (real): average tortuosity of cluster
            
        """
        self.site_indices = site_indices
        self.periodic = None
        self.tortuosity = None
        self.size = size