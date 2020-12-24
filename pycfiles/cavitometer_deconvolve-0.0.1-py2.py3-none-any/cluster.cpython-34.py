# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/caviar/domain/cluster.py
# Compiled at: 2017-10-25 18:02:55
# Size of source mod 2**32: 1202 bytes
__doc__ = '\nCluster module.\n'
import caviar.domain.instance

class Cluster:
    """Cluster"""

    def __init__(self, context, name):
        self._Cluster__context = context
        self._Cluster__name = name

    def __eq__(self, other):
        return self._Cluster__name == other._Cluster__name

    @property
    def name(self):
        """
                Node name.
                
                :rtype:
                   str
                """
        return self._Cluster__name


def restore(context, name, resource):
    return Cluster(context, name)