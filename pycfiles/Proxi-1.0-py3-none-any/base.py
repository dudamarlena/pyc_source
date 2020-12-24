# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /mnt/c/Users/dave/Projects/Github/proxenos/src/proxenos/mappers/base.py
# Compiled at: 2017-01-23 19:48:54
__doc__ = 'Provides a base interface for node cluster data mappers.\n\nNode clusters, or a set of :class:`~.node.Service`, to be specific, are\na pool of socket addresses representing remote services. Cluster mappers\nimplement the data mapper pattern, reading service socket addresses from\nsources such as service discovery tools (i.e. Consul, etcd, or\nZooKeeper) into a set of :class:`~.node.Service`.\n\n.. note::\n\n   Cluster mappers are **not** thread-safe.\n\n'
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