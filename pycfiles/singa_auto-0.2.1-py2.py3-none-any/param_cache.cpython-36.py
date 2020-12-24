# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/singa_auto/redis/param_cache.py
# Compiled at: 2020-04-23 12:22:03
# Size of source mod 2**32: 13133 bytes
import json, numpy as np
from typing import Dict
import uuid, logging
from collections import namedtuple
import msgpack
from datetime import datetime
import traceback
from singa_auto.model import Params
from singa_auto.advisor import ParamsType
from singa_auto.utils.local_cache import LocalCache
from .redis import RedisSession
logger = logging.getLogger(__name__)

class InvalidParamsError(Exception):
    pass


class InvalidParamsFormatError(Exception):
    pass


REDIS_NAMESPACE = 'PARAMS'
PARAM_DATA_TYPE_SEPARATOR = '//'
PARAM_DATA_TYPE_NUMPY = 'NP'
_ParamMeta = namedtuple('_ParamMeta', ('param_id', 'score', 'time'))

class ParamCache(object):
    __doc__ = '\n    Retrieves and caches parameters for a session & a worker, backed by an in-memory cache and Redis for cross-worker sharing (optional).\n\n    :param str session_id: Session ID associated with the parameters\n    '

    def __init__(self, session_id='local', redis_host=None, redis_port=None, cache_size=4):
        self._params = {}
        redis_namespace = f"{REDIS_NAMESPACE}:{session_id}"
        self._redis = RedisSession(redis_namespace, redis_host, redis_port)
        self._local_cache = LocalCache(cache_size)

    def store_params(self, params: Params, score: float=None, time: datetime=None):
        if params is None:
            raise InvalidParamsError('`params` cannot be `None`')
        self._redis.acquire_lock()
        try:
            self._pull_from_redis()
            param_meta = self._update_params_meta(score, time)
            if param_meta:
                self._local_cache.put(param_meta.param_id, params)
            if self._redis:
                self._push_to_redis()
        finally:
            self._redis.release_lock()

    def retrieve_params(self, params_type: ParamsType) -> Params:
        self._redis.acquire_lock()
        try:
            self._pull_from_redis()
            param_id = self._get_params_by_type(params_type)
            if param_id is None:
                return
            logger.info('To use params "{}"'.format(param_id))
            params = self._local_cache.get(param_id)
            if params is not None:
                return params
            params = self._pull_params_from_redis(param_id)
            if params is None:
                logger.error("Params don't exist in Redis!")
                return
            self._local_cache.put(param_id, params)
            return params
        finally:
            self._redis.release_lock()

    def clear_all_params(self):
        self._clear_all_from_redis()

    def _update_params_meta(self, score: float, time: datetime):
        score = score or 0
        time = time or datetime.now()
        param_id = str(uuid.uuid4())
        param_meta = _ParamMeta(param_id, score, time)
        prev_meta = self._params.get('LOCAL_RECENT')
        if prev_meta is None or time >= prev_meta.time:
            self._params['LOCAL_RECENT'] = param_meta
        prev_meta = self._params.get('LOCAL_BEST')
        if prev_meta is None or score >= prev_meta.score:
            self._params['LOCAL_BEST'] = param_meta
        prev_meta = self._params.get('GLOBAL_RECENT')
        if prev_meta is None or time >= prev_meta.time:
            self._params['GLOBAL_RECENT'] = param_meta
        prev_meta = self._params.get('GLOBAL_BEST')
        if prev_meta is None or score >= prev_meta.score:
            self._params['GLOBAL_BEST'] = param_meta
        return param_meta

    def _get_params_by_type(self, params_type: ParamsType) -> str:
        if params_type == ParamsType.NONE:
            return
        else:
            if params_type == ParamsType.LOCAL_RECENT:
                return self._get_local_recent_params()
            else:
                if params_type == ParamsType.LOCAL_BEST:
                    return self._get_local_best_params()
                if params_type == ParamsType.GLOBAL_RECENT:
                    return self._get_global_recent_params()
            if params_type == ParamsType.GLOBAL_BEST:
                return self._get_global_best_params()
        raise InvalidParamsError('No such params type: "{}"'.format(params_type))

    def _get_local_recent_params(self):
        param_meta = self._params.get('LOCAL_RECENT')
        if param_meta is None:
            return
        else:
            return param_meta.param_id

    def _get_local_best_params(self):
        param_meta = self._params.get('LOCAL_BEST')
        if param_meta is None:
            return
        else:
            return param_meta.param_id

    def _get_global_recent_params(self):
        param_meta = self._params.get('GLOBAL_RECENT')
        if param_meta is None:
            return
        else:
            return param_meta.param_id

    def _get_global_best_params(self):
        param_meta = self._params.get('GLOBAL_BEST')
        if param_meta is None:
            return
        else:
            return param_meta.param_id

    def _pull_from_redis(self):
        redis_params = self._pull_metadata_from_redis()
        for param_type, param_meta in redis_params.items():
            self._params[param_type] = param_meta

    def _push_to_redis(self):
        params_to_push = [
         'GLOBAL_BEST', 'GLOBAL_RECENT']
        params_shared = {param_type:param_meta for param_type, param_meta in self._params.items() if param_type in params_to_push}
        redis_params = self._pull_metadata_from_redis()
        og_param_ids = set([x.param_id for x in redis_params.values()])
        new_param_ids = set([x.param_id for x in params_shared.values()])
        to_add = [x for x in new_param_ids if x not in og_param_ids]
        to_delete = [x for x in og_param_ids if x not in new_param_ids]
        for param_id in to_add:
            params = self._local_cache.get(param_id)
            if params:
                self._push_params_to_redis(param_id, params)

        if len(to_delete) > 0:
            (self._delete_params_from_redis)(*to_delete)
        self._push_metadata_to_redis(params_shared)

    def _push_metadata_to_redis(self, params):
        redis_params = {param_type:self._param_meta_to_jsonable(param_meta) for param_type, param_meta in params.items()}
        metadata = {'params': redis_params}
        logger.info('Pushing metadata to Redis: {}...'.format(metadata))
        metadata_str = json.dumps(metadata)
        self._redis.set('meta', metadata_str)

    def _pull_metadata_from_redis(self):
        metadata_str = self._redis.get('meta')
        if metadata_str is not None:
            metadata = json.loads(metadata_str)
            logger.info('Pulled metadata from Redis: {}'.format(metadata))
            params = metadata.get('params', {})
            params = {param_type:self._jsonable_to_param_meta(jsonable) for param_type, jsonable in params.items()}
            return params
        else:
            return {}

    def _delete_params_from_redis(self, *param_ids):
        logger.info('Deleting params: {}...'.format(param_ids))
        param_names = ['params:{}'.format(x) for x in param_ids]
        (self._redis.delete)(*param_names)

    def _clear_all_from_redis(self):
        logger.info('Clearing metadata and params from Redis...')
        self._redis.delete('meta')
        self._redis.delete_pattern('params:*')

    def _push_params_to_redis(self, param_id: str, params: Params):
        logger.info('Pushing params: "{}"...'.format(param_id))
        param_name = 'params:{}'.format(param_id)
        params_bytes = _serialize_params(params)
        self._redis.set(param_name, params_bytes)

    def _pull_params_from_redis(self, param_id: str) -> Params:
        logger.info('Pulling params: "{}"...'.format(param_id))
        param_name = 'params:{}'.format(param_id)
        params_bytes = self._redis.get(param_name)
        if params_bytes is None:
            return
        else:
            params = _deserialize_params(params_bytes)
            return params

    def _param_meta_to_jsonable(self, param_meta: _ParamMeta):
        jsonable = param_meta._asdict()
        jsonable['time'] = str(jsonable['time'])
        return jsonable

    def _jsonable_to_param_meta(self, jsonable):
        jsonable['time'] = datetime.strptime(jsonable['time'], '%Y-%m-%d %H:%M:%S.%f')
        param_meta = _ParamMeta(**jsonable)
        return param_meta


def _serialize_params(params):
    params_simple = _simplify_params(params)
    params_bytes = msgpack.packb(params_simple, use_bin_type=True)
    return params_bytes


def _deserialize_params(params_bytes):
    params_simple = msgpack.unpackb(params_bytes, raw=False)
    params = _unsimplify_params(params_simple)
    return params


def _simplify_params(params):
    try:
        params_simple = {}
        assert isinstance(params, dict)
        for name, value in params.items():
            if not isinstance(name, str):
                raise AssertionError
            else:
                assert PARAM_DATA_TYPE_SEPARATOR not in name
                if isinstance(value, np.ndarray):
                    name = f"{PARAM_DATA_TYPE_NUMPY}{PARAM_DATA_TYPE_SEPARATOR}{name}"
                    value = value.tolist()
                elif not isinstance(value, (str, float, int)):
                    raise AssertionError
            params_simple[name] = value

        return params_simple
    except:
        traceback.print_stack()
        raise InvalidParamsFormatError()


def _unsimplify_params(params_simple):
    params = {}
    for name, value in params_simple.items():
        if PARAM_DATA_TYPE_SEPARATOR in name:
            type_id, name = name.split(PARAM_DATA_TYPE_SEPARATOR)
            if type_id == PARAM_DATA_TYPE_NUMPY:
                value = np.array(value)
        params[name] = value

    return params