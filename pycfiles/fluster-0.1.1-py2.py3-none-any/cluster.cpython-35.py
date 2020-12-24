# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dan/repos/parsely/fluster/fluster/cluster.py
# Compiled at: 2016-01-05 13:47:17
# Size of source mod 2**32: 5772 bytes
from collections import defaultdict
import functools, logging, mmh3, redis
from redis.exceptions import ConnectionError
from .exceptions import ClusterEmptyError
from .penalty_box import PenaltyBox
log = logging.getLogger(__name__)

class FlusterCluster(object):
    __doc__ = "A pool of redis instances where dead nodes are automatically removed.\n\n    This implementation is VERY LIMITED. There is NO consistent hashing, and\n    no attempt at recovery/rebalancing as nodes are dropped/added. Therefore,\n    it's best served for fundamentally ephemeral data where some duplication\n    or missing keys isn't a problem.\n\n    Ideal cases for this are things like caches, where another copy of data\n    isn't a huge problem (provided expiries are respected).\n    "

    @classmethod
    def from_settings(cls, conn_settingses):
        return cls(redis.Redis(**c) for c in conn_settingses)

    def __init__(self, clients, penalty_box_min_wait=10, penalty_box_max_wait=300, penalty_box_wait_multiplier=1.5):
        self.penalty_box = PenaltyBox(min_wait=penalty_box_min_wait, max_wait=penalty_box_max_wait, multiplier=penalty_box_wait_multiplier)
        self.active_clients = self._prep_clients(clients)
        self.initial_clients = {c.pool_id:c for c in clients}
        self._sort_clients()

    def _sort_clients(self):
        """Make sure clients are sorted consistently for consistent results."""
        self.active_clients.sort(key=lambda c: c.pool_id)

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
                """Simple wrapper for to catch dead clients."""
                try:
                    return fn(*args, **kwargs)
                except ConnectionError:
                    if client in self.active_clients:
                        log.warning('%r marked down.', client)
                        self.active_clients.remove(client)
                        self.penalty_box.add(client)
                    raise

            return functools.update_wrapper(wrapper, fn)

        for name in dir(client):
            if name.startswith('_'):
                pass
            else:
                if name in ('echo', 'execute_command', 'parse_response'):
                    pass
                else:
                    obj = getattr(client, name)
                    if not callable(obj):
                        pass
                    else:
                        log.debug('Wrapping %s', name)
                        setattr(client, name, wrap(obj))

    def get_client(self, shard_key):
        """Get the client for a given shard, based on what's available.

        If the proper client isn't available, the next available client
        is returned. If no clients are available, an exception is raised.
        """
        added = False
        for client in self.penalty_box.get():
            log.info('Client %r is back up.', client)
            self.active_clients.append(client)
            added = True

        if added:
            self._sort_clients()
        if len(self.active_clients) == 0:
            raise ClusterEmptyError('All clients are down.')
        if not isinstance(shard_key, bytes):
            shard_key = shard_key.encode('utf-8')
        hashed = mmh3.hash(shard_key)
        pos = hashed % len(self.initial_clients)
        if self.initial_clients[pos] in self.active_clients:
            return self.initial_clients[pos]
        else:
            pos = hashed % len(self.active_clients)
            return self.active_clients[pos]

    def zrevrange_with_int_score(self, key, max_score, min_score):
        """Get the zrevrangebyscore across the cluster.
        Highest score for duplicate element is returned.
        A faster method should be written if scores are not needed.
        """
        if len(self.active_clients) == 0:
            raise ClusterEmptyError('All clients are down.')
        element__score = defaultdict(int)
        for client in self.active_clients:
            revrange = client.zrevrangebyscore(key, max_score, min_score, withscores=True, score_cast_func=int)
            for element, count in revrange:
                element__score[element] = max(element__score[element], int(count))

        return element__score