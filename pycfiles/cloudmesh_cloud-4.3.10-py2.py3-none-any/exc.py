# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/exc.py
# Compiled at: 2017-04-23 10:30:41
__doc__ = '\nThis module contains the exceptions\n'

class UnrecoverableErrorException(Exception):
    """Occurs on an error that cannot be recovered automatically.
    Requires user interaction to change the state.
    """


class NoActiveClusterException(Exception):
    """Occurs when an active cluster is requested but non is set_cloud"""


class ClusterNameClashException(Exception):
    """Occurs when a cluster is created with a preexisting name
    """

    def __init__(self, tablename, name):
        self.tablename = tablename
        self.name = name

    def __str__(self):
        return ('Cluster {} already exists').format(self.name)