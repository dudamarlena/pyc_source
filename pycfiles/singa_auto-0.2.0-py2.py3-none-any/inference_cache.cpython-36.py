# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/singa_auto/redis/inference_cache.py
# Compiled at: 2020-04-23 12:22:03
# Size of source mod 2**32: 4360 bytes
from typing import Union, List
import pickle, logging
from singa_auto.predictor import Prediction, Query
from .redis import RedisSession
logger = logging.getLogger(__name__)
REDIS_NAMESPACE = 'INFERENCE'

class InferenceCache:
    __doc__ = '\n    Caches queries & predictions to facilitate communication between predictor & inference workers.\n\n    For each session, assume a single predictor and multiple inference workers running concurrently.\n\n    :param str session_id: Associated session ID\n    '

    def __init__(self, session_id='local', redis_host=None, redis_port=None):
        redis_namespace = f"{REDIS_NAMESPACE}:{session_id}"
        self._redis = RedisSession(redis_namespace, redis_host, redis_port)

    def get_workers(self) -> List[str]:
        worker_ids = self._redis.list_set('workers')
        return worker_ids

    def add_queries_for_worker(self, worker_id: str, queries: List[Query]):
        name = f"workers:{worker_id}:queries"
        queries = [pickle.dumps(x) for x in queries]
        logger.info(f'Adding {len(queries)} querie(s) for worker "{worker_id}"...')
        (self._redis.prepend_to_list)(name, *queries)

    def take_prediction_for_worker(self, worker_id: str, query_id: str) -> Union[(Prediction, None)]:
        name = f"workers:{worker_id}:{query_id}:prediction"
        prediction = self._redis.get(name)
        if prediction is None:
            return
        else:
            self._redis.delete(name)
            prediction = pickle.loads(prediction)
            logger.info(f'Took prediction for query "{query_id}" from worker "{worker_id}"')
            return prediction

    def clear_all(self):
        self._redis.delete('workers')
        self._redis.delete_pattern('workers:*')
        self._redis.delete_pattern('queries:*')

    def add_worker(self, worker_id: str):
        self._redis.add_to_set('workers', worker_id)

    def pop_queries_for_worker(self, worker_id: str, batch_size: int) -> List[Query]:
        name = f"workers:{worker_id}:queries"
        queries = []
        for _ in range(batch_size):
            query = self._redis.pop_from_list(name)
            if query is None:
                break
            query = pickle.loads(query)
            queries.append(query)

        if len(queries) > 0:
            logger.info(f'Popped {len(queries)} querie(s) for worker "{worker_id}"')
        return queries

    def add_predictions_for_worker(self, worker_id: str, predictions: List[Prediction]):
        logger.info(f'Adding {len(predictions)} prediction(s) for worker "{worker_id}"')
        for prediction in predictions:
            name = f"workers:{worker_id}:{prediction.query_id}:prediction"
            prediction = pickle.dumps(prediction)
            self._redis.set(name, prediction)

    def delete_worker(self, worker_id: str):
        self._redis.delete_from_set('workers', worker_id)