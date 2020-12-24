# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\floscraper\cache.py
# Compiled at: 2019-08-03 22:42:04
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
__author__ = b'd01'
__email__ = b'jungflor@gmail.com'
__copyright__ = b'Copyright (C) 2017-19, Florian JUNG'
__license__ = b'MIT'
__version__ = b'0.2.1'
__date__ = b'2019-08-04'
import datetime, os, abc, threading, logging, hashlib
from io import open
from flotils import Loadable
try:
    import portalocker as porta
except ImportError:
    porta = None

from .models import CacheInfo
_cache = {}
_cache_lock = threading.RLock()
if porta is None:
    logging.warning(b'Not using portalocker')

def now_utc():
    """
    Get current time as utc with tzinfo

    :return: Current time
    :rtype: datetime.datetime
    """
    return datetime.datetime.utcnow()


class Cache(Loadable):
    """ Cache element """
    __metaclass__ = abc.ABCMeta

    def __init__(self, settings=None):
        if settings is None:
            settings = {}
        super(Cache, self).__init__(settings)
        self._duration = datetime.timedelta()
        self.duration = settings.get(b'duration', 420)
        self.use_advanced = settings.get(b'use_advanced', True)
        return

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value):
        if not isinstance(value, datetime.timedelta):
            value = datetime.timedelta(seconds=value)
        self._duration = value

    def prepare_headers(self, headers, cache_info=None):
        """
        Prepare headers object for request (add cache information

        :param headers: Headers object
        :type headers: dict
        :param cache_info: Cache information to add
        :type cache_info: floscraper.models.CacheInfo
        :return: Prepared headers
        :rtype: dict
        """
        if self.use_advanced and cache_info:
            hkeys = headers.keys()
            if cache_info.access_time and b'If-Modified-Since' not in hkeys:
                headers[b'If-Modified-Since'] = cache_info.access_time.strftime(b'%a, %d %b %Y %H:%M:%S GMT')
            if cache_info.etag and b'If-None-Match' not in hkeys:
                headers[b'If-None-Match'] = cache_info.etag
        return headers

    @abc.abstractmethod
    def _cache_meta_get(self, key):
        raise NotImplementedError()

    @abc.abstractmethod
    def _cache_get(self, key):
        raise NotImplementedError()

    @abc.abstractmethod
    def _cache_meta_set(self, key, val):
        raise NotImplementedError()

    @abc.abstractmethod
    def _cache_set(self, key, val):
        raise NotImplementedError()

    def get(self, url, ignore_access_time=False):
        """
        Try to retrieve url from cache if available

        :param url: Url to retrieve
        :type url: str | unicode
        :param ignore_access_time: Should ignore the access time
        :type ignore_access_time: bool
        :return: (data, CacheInfo)
            None, None -> not found in cache
            None, CacheInfo -> found, but is expired
            data, CacheInfo -> found in cache
        :rtype: (None | str | unicode, None | floscraper.models.CacheInfo)
        """
        key = hashlib.md5(url.encode(b'utf-8')).hexdigest()
        accessed = self._cache_meta_get(key)
        if not accessed:
            self.debug((b'From inet {}').format(url))
            return (None, None)
        else:
            if isinstance(accessed, dict):
                cached = CacheInfo.from_dict(accessed)
            else:
                cached = CacheInfo(accessed)
            now = now_utc()
            if now - cached.access_time > self.duration and not ignore_access_time:
                self.debug((b'From inet (expired) {}').format(url))
                return (
                 None, cached)
            try:
                res = self._cache_get(key)
            except:
                self.debug((b'From inet (failure) {}').format(url))
                self.exception(b'Failed to read cache')
                return (None, None)

            self.debug((b'From cache {}').format(url))
            return (res, cached)

    def update(self, url, cache_info=None):
        """
        Update cache information for url

        :param url: Update for this url
        :type url: str | unicode
        :param cache_info: Cache info
        :type cache_info: floscraper.models.CacheInfo
        :rtype: None
        """
        key = hashlib.md5(url.encode(b'utf-8')).hexdigest()
        access_time = None
        if not cache_info:
            cache_info = CacheInfo()
        if not access_time:
            cache_info.access_time = now_utc()
        self._cache_meta_set(key, cache_info.to_dict())
        return

    def put(self, url, html, cache_info=None):
        """
        Put response into cache

        :param url: Url to cache
        :type url: str | unicode
        :param html: HTML content of url
        :type html: str | unicode
        :param cache_info: Cache Info (default: None)
        :type cache_info: floscraper.models.CacheInfo
        :rtype: None
        """
        key = hashlib.md5(url.encode(b'utf-8')).hexdigest()
        try:
            self._cache_set(key, html)
        except:
            self.exception(b'Failed to write cache')
            return

        self.update(url, cache_info)


class NullCache(Cache):
    """ Non caching cache """

    def _cache_meta_get(self, key):
        pass

    def _cache_get(self, key):
        pass

    def _cache_set(self, key, val):
        pass

    def _cache_meta_set(self, key, val):
        pass

    def get(self, url, ignore_access_time=False):
        return (None, None)

    def update(self, url, cache_info=None):
        pass

    def put(self, url, html, cache_info=None):
        pass


class FileCache(Cache):

    def __init__(self, settings=None):
        if settings is None:
            settings = {}
        super(FileCache, self).__init__(settings)
        self._dir = settings[b'directory']
        self._index_path = settings.get(b'index', os.path.join(self._dir, b'cache_index.tmp'))
        self._index = None
        with _cache_lock:
            self._index = _cache
        return

    def _init_index(self):
        if not self._index:
            if os.path.exists(self._index_path):
                try:
                    with open(self._index_path, b'r', encoding=b'utf-8') as (f):
                        if porta:
                            porta.lock(f, porta.LOCK_EX)
                        self._index = self._load_json_file(f)
                except IOError as e:
                    if str(e) != b'Decoding json failed':
                        self.exception(b'Failed to load cache file')
                except:
                    self.exception(b'Failed to load cache file')

            else:
                self.warning((b'Cache index does not exist ({})').format(self._index_path))
        if not self._index:
            self._index = {b'version': b'1.0'}

    def _cache_meta_get(self, key):
        with _cache_lock:
            _cache.update(self._index)
            return _cache.get(key, None)
        return

    def _cache_get(self, key):
        tmp_path = os.path.join(self._dir, key + b'.tmp')
        with open(tmp_path, b'r', encoding=b'utf-8') as (f):
            if porta:
                porta.lock(f, porta.LOCK_EX)
            return f.read()

    def _cache_meta_set(self, key, val):
        self._index[key] = val
        with _cache_lock:
            _cache[key] = self._index[key]

    def _cache_set(self, key, val):
        tmp_path = os.path.join(self._dir, key + b'.tmp')
        with open(tmp_path, b'w', encoding=b'utf-8') as (f):
            if porta:
                porta.lock(f, porta.LOCK_EX)
            f.write(val)
            f.flush()

    def get(self, url, ignore_access_time=False):
        if not self._dir:
            self.debug((b'From inet {}').format(url))
            return (None, None, None)
        else:
            self._init_index()
            return super(FileCache, self).get(url, ignore_access_time)

    def put(self, url, html, cache_info=None):
        if not self._dir:
            return
        super(FileCache, self).put(url, html, cache_info)
        try:
            with open(self._index_path, b'w', encoding=b'utf-8') as (f):
                with _cache_lock:
                    if porta:
                        porta.lock(f, porta.LOCK_EX)
                    self._save_json_file(f, _cache)
                    f.flush()
        except:
            self.exception(b'Failed to save cache')