# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/caviar/domain/cluster.py
# Compiled at: 2017-10-25 18:02:55
# Size of source mod 2**32: 1202 bytes
"""
Cluster module.
"""
import caviar.domain.instance

class Cluster:
    __doc__ = '\n\tCluster.\n\n\t:param caviar.domain.ManagedDomainContext context:\n\t   Managed domain context.\n\t:param str name:\n\t   Cluster name.\n\t'

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