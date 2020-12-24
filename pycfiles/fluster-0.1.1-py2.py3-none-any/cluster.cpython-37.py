# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dan/Documents/repos/parsely/fluster/fluster/cluster.py
# Compiled at: 2019-04-24 11:39:54
# Size of source mod 2**32: 7194 bytes
from collections import defaultdict
from itertools import cycle
import functools, logging, mmh3, redis
from redis.exceptions import ConnectionError, TimeoutError
from .exceptions import ClusterEmptyError
from .penalty_box import PenaltyBox
log = logging.getLogger(__name__)

class FlusterCluster(object):
    __doc__ = "A pool of redis instances where dead nodes are automatically removed.\n\n    This implementation is VERY LIMITED. There is NO consistent hashing, and\n    no attempt at recovery/rebalancing as nodes are dropped/added. Therefore,\n    it's best served for fundamentally ephemeral data where some duplication\n    or missing keys isn't a problem.\n\n    Ideal cases for this are things like caches, where another copy of data\n    isn't a huge problem (provided expiries are respected).\n\n    The FlusterCluster instance can be iterated through, and only active\n    connections will be returned.\n    "

    @classmethod
    def from_settings(cls, conn_settingses):
        return cls(((redis.Redis)(**c) for c in conn_settingses))

    def __init__(self, clients, penalty_box_min_wait=10, penalty_box_max_wait=300, penalty_box_wait_multiplier=1.5):
        self.penalty_box = PenaltyBox(min_wait=penalty_box_min_wait, max_wait=penalty_box_max_wait,
          multiplier=penalty_box_wait_multiplier)
        self.active_clients = self._prep_clients(clients)
        self.initial_clients = {c.pool_id:c for c in clients}
        self.clients = cycle(self.initial_clients.values())
        self._sort_clients()

    def __iter__(self):
        """Updates active clients each time it's iterated through."""
        self._prune_penalty_box()
        return self

    def __next__(self):
        """Always returns a client, or raises an Exception if none are available."""
        if len(self.active_clients) == 0:
            raise ClusterEmptyError('All clients are down.')
        self._prune_penalty_box()
        for client in self.clients:
            if client in self.active_clients:
                return client

    def next(self):
        """Python 2/3 compatibility."""
        return self.__next__()

    def _sort_clients(self):
        """Make sure clients are sorted consistently for consistent results."""
        self.active_clients.sort(key=(lambda c: c.pool_id))

    def _prep_clients(self, clients):
        """Prep a client by tagging it with and id and wrapping methods.

        Methods are wrapper to catch ConnectionError so that we can remove
        it from the pool until the instance comes back up.

        :returns: patched clients
        """
        for pool_id, client in enumerate(clients):
            if hasattr(client, 'pool_id'):
                raise ValueError('%r is already part of a pool.', client)
            setattr(client, 'pool_id', pool_id)
            self._wrap_functions(client)

        return clients

    def _wrap_functions(self, client):
        """Wrap public functions to catch ConnectionError.

        When an error happens, it puts the client in the penalty box
        so that it won't be retried again for a little while.
        """

        def wrap(fn):

            def wrapper(*args, **kwargs):
                try:
                    return fn(*args, **kwargs)
                except (ConnectionError, TimeoutError):
                    self._penalize_client(client)
                    raise

            return functools.update_wrapper(wrapper, fn)

        for name in dir(client):
            if name.startswith('_'):
                continue
            if name in ('echo', 'execute_command', 'parse_response'):
                continue
            obj = getattr(client, name)
            if not callable(obj):
                continue
            log.debug('Wrapping %s', name)
            setattr(client, name, wrap(obj))

    def _prune_penalty_box(self):
        """Restores clients that have reconnected.

        This function should be called first for every public method.
        """
        added = False
        for client in self.penalty_box.get():
            log.info('Client %r is back up.', client)
            self.active_clients.append(client)
            added = True

        if added:
            self._sort_clients()

    def get_client(self, shard_key):
        """Get the client for a given shard, based on what's available.

        If the proper client isn't available, the next available client
        is returned. If no clients are available, an exception is raised.
        """
        self._prune_penalty_box()
        if len(self.active_clients) == 0:
            raise ClusterEmptyError('All clients are down.')
        if not isinstance(shard_key, bytes):
            shard_key = shard_key.encode('utf-8')
        hashed = mmh3.hash(shard_key)
        pos = hashed % len(self.initial_clients)
        if self.initial_clients[pos] in self.active_clients:
            return self.initial_clients[pos]
        pos = hashed % len(self.active_clients)
        return self.active_clients[pos]

    def _penalize_client(self, client):
        """Place client in the penalty box.

        :param client: Client object
        """
        if client in self.active_clients:
            log.warning('%r marked down.', client)
            self.active_clients.remove(client)
            self.penalty_box.add(client)
        else:
            log.info('%r not in active client list.')

    def zrevrange_with_int_score(self, key, max_score, min_score):
        """Get the zrevrangebyscore across the cluster.
        Highest score for duplicate element is returned.
        A faster method should be written if scores are not needed.
        """
        self._prune_penalty_box()
        if len(self.active_clients) == 0:
            raise ClusterEmptyError('All clients are down.')
        element__score = defaultdict(int)
        for client in self.active_clients:
            revrange = client.zrevrangebyscore(key,
              max_score, min_score, withscores=True,
              score_cast_func=int)
            for element, count in revrange:
                element__score[element] = max(element__score[element], int(count))

        return element__score