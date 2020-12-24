# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/exc.py
# Compiled at: 2017-04-23 10:30:41
"""
This module contains the exceptions
"""

class UnrecoverableErrorException(Exception):
    """Occurs on an error that cannot be recovered automatically.
    Requires user interaction to change the state.
    """
    pass


class NoActiveClusterException(Exception):
    """Occurs when an active cluster is requested but non is set_cloud"""
    pass


class ClusterNameClashException(Exception):
    """Occurs when a cluster is created with a preexisting name
    """

    def __init__(self, tablename, name):
        self.tablename = tablename
        self.name = name

    def __str__(self):
        return ('Cluster {} already exists').format(self.name)