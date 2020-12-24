# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/cache/base.py
# Compiled at: 2017-01-22 12:23:30
from __future__ import unicode_literals
from __future__ import print_function
from .. import errors
from ..tools import DummyLock
from ..context.expressiontime import TimeSpan
from ..containers import LRUCache
from ..compat import pickle, text_type, binary_type, with_metaclass, implements_to_string, PY3
from threading import Lock
from time import time
import zlib, hashlib, logging
log = logging.getLogger(b'moya.cache')

class CacheMeta(type):
    cache_backends = {}

    def __new__(cls, name, base, attrs):
        new_class = type.__new__(cls, name, base, attrs)
        if name != b'CacheBase':
            name = getattr(new_class, b'cache_backend_name', name.lower().strip(b'_'))
            cls.cache_backends[name] = new_class
        return new_class


_not_present = object()

class CacheType(object):
    """
    Very simple cache layer

    Cache objects are designed to be very robust.
    All exceptions are trapped so that if a cache fails for whatever reason, the server
    will continue to serve requests (albeit with reduced performance). Any unknown exceptions
    are logged to moya.runtime.

    """
    enabled = True
    max_key_length = 250

    def __init__(self, name, namespace, thread_safe=False, compress=False, compress_min=1024):
        self.name = name
        self.ns = namespace or b''
        self.compress = compress
        self.compress_min = compress_min
        if thread_safe:
            self.lock = DummyLock()
        else:
            self.lock = Lock()
        self._key_cache = LRUCache(1000)

    def __repr__(self):
        return b"<cache:%s '%s'>" % (self.cache_backend_name, self.name)

    @classmethod
    def create(cls, name, settings):
        disabled = not settings.get_bool(b'enabled', True)
        if disabled:
            cache_type = b'disabled'
        else:
            cache_type = settings.get(b'type', b'dict')
        try:
            cache_cls = CacheMeta.cache_backends[cache_type]
        except KeyError:
            types = (b', ').join((b"'{}'").format(k) for k in sorted(CacheMeta.cache_backends.keys()))
            raise errors.StartupFailedError((b"Cache type must be one of {} (not '{}')").format(types, cache_type))

        debug = settings.get_bool(b'debug', False)
        cache = cache_cls.initialize(name, settings)
        if debug:
            cache = DebugCacheWrapper(cache)
        return cache

    @classmethod
    def initialize(cls, name, settings):
        return cls(name, settings.get(b'namespace', b''), compress=settings.get_bool(b'compress', True), compress_min=settings.get_int(b'compress_min', 1024))

    def shorten_key(self, key, max_length=None):
        assert isinstance(key, binary_type), b'key must be bytes'
        if max_length is None:
            max_length = self.max_key_length
        if len(key) > max_length:
            _hash = hashlib.md5()
            _hash.update(key)
            _hash = _hash.hexdigest()
            if PY3:
                _hash = _hash.encode(b'utf-8')
            key = key[:max_length - len(_hash)] + _hash
        return key

    def get_key(self, key):
        """Gets a binary key from a unicode string"""
        try:
            bytes_key = self._key_cache[(self.ns, key)]
        except KeyError:
            bytes_key = self._key_cache[(self.ns, key)] = self._get_key(key)

        return bytes_key

    def _get_key(self, key):
        """Gets a key (binary string) that contains the namespace"""
        key = b'{%s}%s' % (self.ns, key)
        key = self.shorten_key(key.encode(b'utf-8'))
        return key

    def encode_value(self, value):
        """Encodes a value in to a binary string"""
        dump = pickle.dumps(value, pickle.HIGHEST_PROTOCOL)
        if self.compress and len(dump) >= self.compress_min:
            return zlib.compress(dump) + b'ZZ'
        if dump.endswith(b'XX'):
            return dump + b'XX'
        return dump

    def decode_value(self, value):
        """Decodes a value encoded by `encode_value`"""
        if value.endswith(b'ZZ'):
            value = zlib.decompress(value[:-2])
        elif value.endswith(b'XX'):
            value = value[:-2]
        return pickle.loads(value)

    def set(self, k, value, time=0):
        """Set key `k` to `value`, with a max lifespan of `time` milliseconds"""
        time = max(0, time)
        if value is None:
            raise ValueError(b'value may not be None')
        with self.lock:
            try:
                self._set(k, value, time=time)
            except Exception as e:
                log.exception((b'{} SET failed ({})').format(self, e))

        return

    def _set(self, k, value, time):
        """Implementation specifics for `set` method"""
        raise NotImplementedError

    def get(self, k, default=None):
        """Get value for key `k`, or return `default` if the key could not be read"""
        with self.lock:
            try:
                return self._get(k, default)
            except Exception as e:
                log.error((b'{} GET failed ({})').format(self, e))
                return default

    def delete(self, k):
        """Delete the value indexed by `k`"""
        with self.lock:
            try:
                return self._delete(k)
            except Exception as e:
                log.error((b'{} DELETE failed ({})').format(self, e))

    def _delete(self, k):
        raise NotImplementedError

    def _get(self, key, default):
        """Implementation specifics for `get` method"""
        raise NotImplementedError

    def contains(self, k):
        """Check if a given key `k` exists in the cache"""
        with self.lock:
            try:
                return self._contains(k)
            except Exception as e:
                log.error((b'{} CONTAINS failed ({})').format(self, e))
                return False

    def _contains(self, k):
        """Implementation specifics for `contains` method"""
        return self._get(k, None) is not None

    def __contains__(self, k):
        """Enables 'in' operator"""
        return self.contains(k)

    def evict(self):
        """Evict any expired keys"""
        pass


class Cache(with_metaclass(CacheMeta, CacheType)):
    pass


@implements_to_string
class DebugCacheWrapper(object):
    """Wraps a cache object, and logs messages for each call to get/set/delete/contains"""

    def __init__(self, cache):
        self.cache = cache
        self.enabled = cache.enabled
        self.ns = cache.ns

    def __repr__(self):
        return (b'{} (debug)').format(self.cache)

    def _get_debug_value(self, value, size=50):
        debug_value = value
        try:
            if isinstance(debug_value, binary_type):
                debug_value = debug_value.replace(b'\n', b'\\n')
                if len(debug_value) > size:
                    debug_value = debug_value[:size] + b'[...]'
                debug_value = repr(debug_value)
            else:
                debug_value = text_type(value)
                debug_value = debug_value.replace(b'\n', b'\\n')
                if len(debug_value) > size:
                    debug_value = debug_value[:size] + b'[...]'
        except:
            debug_value = b'<unprintable value>'

        return debug_value

    def set(self, k, value, time=0):
        log_msg = (b"{} SET '{}' = {}").format(self.cache, self._get_debug_value(k, 100), self._get_debug_value(value))
        if time:
            log_msg += (b' ({})').format(TimeSpan(time).text)
        log.debug(log_msg)
        return self.cache.set(k, value, time=time)

    def get(self, k, default=None):
        start = time()
        value = self.cache.get(k, default)
        taken = (time() - start) * 1000.0
        log_msg = (b"{} GET '{}' = {} {:.2f}ms").format(self.cache, self._get_debug_value(k, 100), self._get_debug_value(value), taken)
        log.debug(log_msg)
        return value

    def delete(self, k):
        log_msg = (b"{} DELETE '{}'").format(self.cache, self._get_debug_value(k, 100))
        log.debug(log_msg)
        return self.cache.delete(k)

    def contains(self, k):
        contains = self.cache.contains(k)
        log_msg = (b'{} CONTAINS {} ({})').format(self.cache, self._get_debug_value(k, 100), contains)
        log.debug(log_msg)
        return contains

    def __contains__(self, k):
        return self.contains(k)