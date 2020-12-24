# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/singa_auto/redis/train_cache.py
# Compiled at: 2020-04-23 12:22:03
# Size of source mod 2**32: 3991 bytes
from typing import Union, List
import logging
from singa_auto.advisor import Proposal, TrialResult
from .redis import RedisSession
logger = logging.getLogger(__name__)
REDIS_NAMESPACE = 'TRAIN'

class TrainCache(object):
    __doc__ = '\n    Caches proposals and trial results to facilitate communication between advisor & train workers.\n\n    For each session, assume a single advisor and multiple train workers running concurrently.\n\n    :param str session_id: Associated session ID\n    '

    def __init__(self, session_id='local', redis_host=None, redis_port=None):
        redis_namespace = f"{REDIS_NAMESPACE}:{session_id}"
        self._redis = RedisSession(redis_namespace, redis_host, redis_port)

    def get_workers(self) -> List[str]:
        worker_ids = self._redis.list_set('workers') or []
        return worker_ids

    def take_result(self, worker_id) -> Union[(TrialResult, None)]:
        name = f"workers:{worker_id}:result"
        result = self._redis.get(name)
        if result is None:
            return
        else:
            self._redis.delete(name)
            logger.info(f'Retrieved result "{result}" for worker "{worker_id}"')
            return TrialResult.from_jsonable(result)

    def get_proposal(self, worker_id: str) -> Union[(Proposal, None)]:
        name = f"workers:{worker_id}:proposal"
        proposal = self._redis.get(name)
        if proposal is None:
            return
        else:
            proposal = Proposal.from_jsonable(proposal)
            return proposal

    def create_proposal(self, worker_id: str, proposal: Proposal):
        name = f"workers:{worker_id}:proposal"
        assert self._redis.get(name) is None
        logger.info(f'Creating proposal "{proposal}" for worker "{worker_id}"...')
        self._redis.set(name, proposal.to_jsonable())

    def clear_all(self):
        logger.info('Clearing proposals & trial results...')
        self._redis.delete('workers')
        self._redis.delete_pattern('workers:*')

    def add_worker(self, worker_id: str):
        self._redis.add_to_set('workers', worker_id)

    def delete_proposal(self, worker_id: str):
        name = f"workers:{worker_id}:proposal"
        logger.info(f'Deleting existing proposal for worker "{worker_id}"...')
        self._redis.delete(name)

    def delete_worker(self, worker_id: str):
        self._redis.delete_from_set('workers', worker_id)

    def create_result(self, worker_id: str, result: TrialResult):
        name = f"workers:{worker_id}:result"
        assert self._redis.get(name) is None
        logger.info(f'Creating result "{result}" for worker "{worker_id}"...')
        self._redis.set(name, result.to_jsonable())