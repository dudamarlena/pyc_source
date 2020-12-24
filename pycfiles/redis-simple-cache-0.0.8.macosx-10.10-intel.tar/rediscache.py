# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/redis_cache/rediscache.py
# Compiled at: 2015-04-28 13:14:17
"""
A simple redis-cache interface for storing python objects.
"""
from functools import wraps
import pickle, json, hashlib, redis, logging
DEFAULT_EXPIRY = 86400

class RedisConnect(object):
    """
    A simple object to store and pass database connection information.
    This makes the Simple Cache class a little more flexible, for cases
    where redis connection configuration needs customizing.
    """

    def __init__(self, host=None, port=None, db=None, password=None):
        self.host = host if host else 'localhost'
        self.port = port if port else 6379
        self.db = db if db else 0
        self.password = password

    def connect(self):
        """
        We cannot assume that connection will succeed, as such we use a ping()
        method in the redis client library to validate ability to contact redis.
        RedisNoConnException is raised if we fail to ping.
        :return: redis.StrictRedis Connection Object
        """
        try:
            redis.StrictRedis(host=self.host, port=self.port, password=self.password).ping()
        except redis.ConnectionError as e:
            raise RedisNoConnException('Failed to create connection to redis', (
             self.host,
             self.port))

        return redis.StrictRedis(host=self.host, port=self.port, db=self.db, password=self.password)


class CacheMissException(Exception):
    pass


class ExpiredKeyException(Exception):
    pass


class RedisNoConnException(Exception):
    pass


class DoNotCache(Exception):
    _result = None

    def __init__(self, result):
        super(DoNotCache, self).__init__()
        self._result = result

    @property
    def result(self):
        return self._result


class SimpleCache(object):

    def __init__(self, limit=10000, expire=DEFAULT_EXPIRY, hashkeys=False, host=None, port=None, db=None, password=None, namespace='SimpleCache'):
        self.limit = limit
        self.expire = expire
        self.prefix = namespace
        self.host = host
        self.port = port
        self.db = db
        try:
            self.connection = RedisConnect(host=self.host, port=self.port, db=self.db, password=password).connect()
        except RedisNoConnException as e:
            self.connection = None

        self.hashkeys = hashkeys
        return

    def make_key(self, key):
        return ('SimpleCache-{0}:{1}').format(self.prefix, key)

    def namespace_key(self, namespace):
        return self.make_key(namespace + ':*')

    def get_set_name(self):
        return ('SimpleCache-{0}-keys').format(self.prefix)

    def store(self, key, value, expire=None):
        """
        Method stores a value after checking for space constraints and
        freeing up space if required.
        :param key: key by which to reference datum being stored in Redis
        :param value: actual value being stored under this key
        :param expire: time-to-live (ttl) for this datum
        """
        key = to_unicode(key)
        value = to_unicode(value)
        set_name = self.get_set_name()
        while self.connection.scard(set_name) >= self.limit:
            del_key = self.connection.spop(set_name)
            self.connection.delete(self.make_key(del_key))

        pipe = self.connection.pipeline()
        if expire is None:
            expire = self.expire
        if isinstance(expire, int) and expire <= 0:
            pipe.set(self.make_key(key), value)
        else:
            pipe.setex(self.make_key(key), expire, value)
        pipe.sadd(set_name, key)
        pipe.execute()
        return

    def expire_all_in_set(self):
        """
        Method expires all keys in the namespace of this object.
        At times there is  a need to invalidate cache in bulk, because a
        single change may result in all data returned by a decorated function
        to be altered.
        Method returns a tuple where first value is total number of keys in
        the set of this object's namespace and second value is a number of
        keys successfully expired.
        :return: int, int
        """
        all_members = self.keys()
        keys = [ self.make_key(k) for k in all_members ]
        with self.connection.pipeline() as (pipe):
            pipe.delete(*keys)
            pipe.execute()
        return (len(self), len(all_members))

    def expire_namespace(self, namespace):
        """
        Method expires all keys in the namespace of this object.
        At times there is  a need to invalidate cache in bulk, because a
        single change may result in all data returned by a decorated function
        to be altered.
        Method returns a tuple where first value is total number of keys in
        the set of this object's namespace and second value is a number of
        keys successfully expired.
        :return: int, int
        """
        namespace = self.namespace_key(namespace)
        all_members = list(self.connection.keys(namespace))
        with self.connection.pipeline() as (pipe):
            pipe.delete(*all_members)
            pipe.execute()
        return (len(self), len(all_members))

    def isexpired(self, key):
        """
        Method determines whether a given key is already expired. If not expired,
        we expect to get back current ttl for the given key.
        :param key: key being looked-up in Redis
        :return: bool (True) if expired, or int representing current time-to-live (ttl) value
        """
        ttl = self.connection.pttl(('SimpleCache-{0}').format(key))
        if ttl == -2:
            ttl = self.connection.pttl(self.make_key(key))
        elif ttl == -1:
            return True
        if ttl is not None:
            return ttl
        else:
            return self.connection.pttl(('{0}:{1}').format(self.prefix, key))
            return

    def store_json(self, key, value, expire=None):
        self.store(key, json.dumps(value), expire)

    def store_pickle(self, key, value, expire=None):
        self.store(key, pickle.dumps(value), expire)

    def get(self, key):
        key = to_unicode(key)
        if key:
            value = self.connection.get(self.make_key(key))
            if value is None:
                if key not in self:
                    raise CacheMissException
                self.connection.srem(self.get_set_name(), key)
                raise ExpiredKeyException
            else:
                return value
        return

    def mget(self, keys):
        """
        Method returns a dict of key/values for found keys.
        :param keys: array of keys to look up in Redis
        :return: dict of found key/values
        """
        if keys:
            cache_keys = [ self.make_key(to_unicode(key)) for key in keys ]
            values = self.connection.mget(cache_keys)
            if None in values:
                pipe = self.connection.pipeline()
                for cache_key, value in zip(cache_keys, values):
                    if value is None:
                        pipe.srem(self.get_set_name(), cache_key)

                pipe.execute()
            return {k:v for k, v in zip(keys, values) if v is not None if v is not None}
        else:
            return

    def get_json(self, key):
        return json.loads(self.get(key))

    def get_pickle(self, key):
        return pickle.loads(self.get(key))

    def mget_json(self, keys):
        """
        Method returns a dict of key/values for found keys with each value
        parsed from JSON format.
        :param keys: array of keys to look up in Redis
        :return: dict of found key/values with values parsed from JSON format
        """
        d = self.mget(keys)
        if d:
            for key in d.keys():
                d[key] = json.loads(d[key]) if d[key] else None

            return d
        return

    def invalidate(self, key):
        """
        Method removes (invalidates) an item from the cache.
        :param key: key to remove from Redis
        """
        key = to_unicode(key)
        pipe = self.connection.pipeline()
        pipe.srem(self.get_set_name(), key)
        pipe.delete(self.make_key(key))
        pipe.execute()

    def __contains__(self, key):
        return self.connection.sismember(self.get_set_name(), key)

    def __iter__(self):
        if not self.connection:
            return iter([])
        return iter([ ('{0}:{1}').format(self.prefix, x) for x in self.connection.smembers(self.get_set_name())
                    ])

    def __len__(self):
        return self.connection.scard(self.get_set_name())

    def keys(self):
        return self.connection.smembers(self.get_set_name())

    def flush(self):
        keys = list(self.keys())
        keys.append(self.get_set_name())
        with self.connection.pipeline() as (pipe):
            pipe.delete(*keys)
            pipe.execute()

    def flush_namespace(self, space):
        namespace = self.namespace_key(space)
        setname = self.get_set_name()
        keys = list(self.connection.keys(namespace))
        with self.connection.pipeline() as (pipe):
            pipe.delete(*keys)
            pipe.srem(setname, *space)
            pipe.execute()

    def get_hash(self, args):
        if self.hashkeys:
            key = hashlib.md5(args).hexdigest()
        else:
            key = pickle.dumps(args)
        return key


def cache_it(limit=10000, expire=DEFAULT_EXPIRY, cache=None, use_json=False, namespace=None):
    """
    Arguments and function result must be pickleable.
    :param limit: maximum number of keys to maintain in the set
    :param expire: period after which an entry in cache is considered expired
    :param cache: SimpleCache object, if created separately
    :return: decorated function
    """
    cache_ = cache
    expire_ = expire

    def decorator(function):
        cache, expire = cache_, expire_
        if cache is None:
            cache = SimpleCache(limit, expire, hashkeys=True, namespace=function.__module__)
        elif expire == DEFAULT_EXPIRY:
            expire = None

        @wraps(function)
        def func(*args, **kwargs):
            if cache.connection is None:
                result = function(*args, **kwargs)
                return result
            else:
                serializer = json if use_json else pickle
                fetcher = cache.get_json if use_json else cache.get_pickle
                storer = cache.store_json if use_json else cache.store_pickle
                key = cache.get_hash(serializer.dumps([args, kwargs]))
                cache_key = ('{func_name}:{key}').format(func_name=function.__name__, key=key)
                if namespace:
                    cache_key = ('{namespace}:{key}').format(namespace=namespace, key=cache_key)
                try:
                    return fetcher(cache_key)
                except (ExpiredKeyException, CacheMissException) as e:
                    pass
                except:
                    logging.exception('Unknown redis-simple-cache error. Please check your Redis free space.')

                try:
                    result = function(*args, **kwargs)
                except DoNotCache as e:
                    result = e.result
                else:
                    try:
                        storer(cache_key, result, expire)
                    except redis.ConnectionError as e:
                        logging.exception(e)

                return result

        return func

    return decorator


def cache_it_json(limit=10000, expire=DEFAULT_EXPIRY, cache=None, namespace=None):
    """
    Arguments and function result must be able to convert to JSON.
    :param limit: maximum number of keys to maintain in the set
    :param expire: period after which an entry in cache is considered expired
    :param cache: SimpleCache object, if created separately
    :return: decorated function
    """
    return cache_it(limit=limit, expire=expire, use_json=True, cache=cache, namespace=None)


def to_unicode(obj, encoding='utf-8'):
    if isinstance(obj, basestring):
        if not isinstance(obj, unicode):
            obj = unicode(obj, encoding)
    return obj