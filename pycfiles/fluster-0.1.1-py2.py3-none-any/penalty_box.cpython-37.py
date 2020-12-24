# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dan/Documents/repos/parsely/fluster/fluster/penalty_box.py
# Compiled at: 2019-04-24 11:39:54
# Size of source mod 2**32: 1823 bytes
import heapq, logging, time
from redis.exceptions import ConnectionError, TimeoutError
log = logging.getLogger(__name__)

class PenaltyBox(object):
    __doc__ = 'A place for redis clients being put in timeout.'

    def __init__(self, min_wait=10, max_wait=300, multiplier=1.5):
        self._clients = []
        self._client_ids = set()
        self._min_wait = min_wait
        self._max_wait = max_wait
        self._multiplier = multiplier

    def add(self, client):
        """Add a client to the penalty box."""
        if client.pool_id in self._client_ids:
            log.info('%r is already in the penalty box. Ignoring.', client)
            return
        release = time.time() + self._min_wait
        heapq.heappush(self._clients, (release, (client, self._min_wait)))
        self._client_ids.add(client.pool_id)

    def get(self):
        """Get any clients ready to be used.

        :returns: Iterable of redis clients
        """
        now = time.time()
        while self._clients and self._clients[0][0] < now:
            _, (client, last_wait) = heapq.heappop(self._clients)
            connect_start = time.time()
            try:
                client.echo('test')
                self._client_ids.remove(client.pool_id)
                yield client
            except (ConnectionError, TimeoutError):
                timer = time.time() - connect_start
                wait = min(int(last_wait * self._multiplier), self._max_wait)
                heapq.heappush(self._clients, (
                 time.time() + wait, (client, wait)))
                log.info('%r is still down after a %s second attempt to connect. Retrying in %ss.', client, timer, wait)