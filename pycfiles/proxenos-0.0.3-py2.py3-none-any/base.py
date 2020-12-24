# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/dave/Projects/Github/proxenos/src/proxenos/mappers/base.py
# Compiled at: 2017-01-23 19:48:54
"""Provides a base interface for node cluster data mappers.

Node clusters, or a set of :class:`~.node.Service`, to be specific, are
a pool of socket addresses representing remote services. Cluster mappers
implement the data mapper pattern, reading service socket addresses from
sources such as service discovery tools (i.e. Consul, etcd, or
ZooKeeper) into a set of :class:`~.node.Service`.

.. note::

   Cluster mappers are **not** thread-safe.

"""
from __future__ import absolute_import
import abc, typing, attr, six, proxenos.node, proxenos.rendezvous
__all__ = ('BaseClusterMapper', )

@attr.s
@six.add_metaclass(abc.ABCMeta)
class BaseClusterMapper(object):
    """Serializes services into a set of :class:`~.node.Service`."""
    host = attr.ib()
    port = attr.ib(convert=int)
    cluster = attr.ib(default=attr.Factory(set), convert=set, repr=False)
    _conn = attr.ib(default=attr.NOTHING, repr=False, hash=False, init=False)

    def __attrs_post_init__(self):
        self._conn = self.make_connection()

    @abc.abstractmethod
    def make_connection(self):
        """Returns a connection to a service discovery system."""
        pass

    @abc.abstractmethod
    def update(self):
        """Reads all service nodes into the socket address cluster."""
        pass

    def select(self, key, hash_method, **hash_options):
        """Selects a node from the cluster based using HRW hashing.

        Args:
            key (str or int): An arbitrary hashable object, typically a
                string or integer.
            hash_method (:class:`HashMethod`): The pseudorandom function
                (PRF) or hash function to use. Defaults to
                :attr:`HashMethod.SIPHASH`.
            **hash_options: Additional parameters to pass to the hash
                function, such as seed, salt, or key length.

        Returns:
            The :class:`Service` of the selected node.

        """
        return proxenos.rendezvous.select_node(self.cluster, key)