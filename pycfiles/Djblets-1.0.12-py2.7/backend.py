# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/cache/backend.py
# Compiled at: 2019-06-12 01:17:17
"""Utility functions for working with memory caching backends.

These functions are designed to integrate with a cache backend using
Django's cache framework. They handle creating caching keys unique to the
install and caching more complex data efficiently (such as the results of
iterators and large data normally too big for the cache).
"""
from __future__ import unicode_literals
from hashlib import md5
import logging, zlib
from django.conf import settings
from django.core.cache import cache
from django.contrib.sites.models import Site
from django.utils import six
from django.utils.six.moves import range, cPickle as pickle, cStringIO as StringIO
from djblets.cache.errors import MissingChunkError
DEFAULT_EXPIRATION_TIME = 2592000
CACHE_CHUNK_SIZE = 1047552
MAX_KEY_SIZE = 240
logger = logging.getLogger(__name__)
_default_expiration = getattr(settings, b'CACHE_EXPIRATION_TIME', DEFAULT_EXPIRATION_TIME)

def _cache_fetch_large_data(cache, key, compress_large_data):
    """Fetch large data from the cache.

    The main cache key indicating the number of chunks will be read, followed
    by each of the chunks. If any chunks are missing, a MissingChunkError
    will be immediately returned.

    The data is then combined and optionally uncompressed, and returned to
    the caller. The caller should iterate through the results using
    _cache_iter_large_data.
    """
    chunk_count = int(cache.get(make_cache_key(key)))
    chunk_keys = [ make_cache_key(b'%s-%d' % (key, i)) for i in range(chunk_count)
                 ]
    chunks = cache.get_many(chunk_keys)
    if len(chunks) != chunk_count:
        missing_keys = sorted(set(chunk_keys) - set(six.iterkeys(chunks)))
        logger.debug(b'Cache miss for key(s): %s.' % (b', ').join(missing_keys))
        raise MissingChunkError
    data = (b'').join(chunks[chunk_key][0] for chunk_key in chunk_keys)
    if compress_large_data:
        data = zlib.decompress(data)
    return data


def _cache_iter_large_data(data, key):
    """Iterate through large data that was fetched from the cache.

    This will unpickle the large data previously fetched through
    _cache_fetch_large_data, and yield each object to the caller.
    """
    fp = StringIO(data)
    try:
        while True:
            try:
                yield pickle.load(fp)
            except EOFError:
                return

    except Exception as e:
        logger.warning(b'Unpickle error for cache key "%s": %s.' % (key, e))
        raise


def _cache_compress_pickled_data(items):
    """Compress lists of items for storage in the cache.

    This works with generators, and will take each item in the list or
    generator of items, zlib-compress the data, and store it in a buffer.The
    item and a blob of compressed data will be yielded to the caller.
    """
    compressor = zlib.compressobj()
    for data, has_item, item in items:
        yield (compressor.compress(data), has_item, item)

    remaining = compressor.flush()
    if remaining:
        yield (
         remaining, False, None)
    return


def _cache_store_chunks(items, key, expiration):
    """Store a list of items as chunks in the cache.

    The list of items will be combined into chunks and stored in the
    cache as efficiently as possible. Each item in the list will be
    yielded to the caller as it's fetched from the list or generator.
    """
    chunks_data = StringIO()
    chunks_data_len = 0
    read_start = 0
    item_count = 0
    i = 0
    for data, has_item, item in items:
        if has_item:
            yield item
            item_count += 1
        chunks_data.write(data)
        chunks_data_len += len(data)
        if chunks_data_len > CACHE_CHUNK_SIZE:
            chunks_data.seek(read_start)
            cached_data = {}
            while chunks_data_len > CACHE_CHUNK_SIZE:
                chunk = chunks_data.read(CACHE_CHUNK_SIZE)
                chunk_len = len(chunk)
                chunks_data_len -= chunk_len
                read_start += chunk_len
                cached_data[make_cache_key(b'%s-%d' % (key, i))] = [
                 chunk]
                i += 1

            cache.set_many(cached_data, expiration)
            chunks_data.seek(0, 2)

    if chunks_data_len > 0:
        assert chunks_data_len <= CACHE_CHUNK_SIZE
        chunks_data.seek(read_start)
        chunk = chunks_data.read()
        cache.set(make_cache_key(b'%s-%d' % (key, i)), [chunk], expiration)
        i += 1
    cache.set(make_cache_key(key), b'%d' % i, expiration)


def _cache_store_items(cache, key, items, expiration, compress_large_data):
    """Store items in the cache.

    The items will be individually pickled and combined into a binary blob,
    which can then optionally be compressed. The resulting data is then
    cached over one or more keys, each representing a chunk about 1MB in size.

    A main cache key will be set that contains information on the other keys.
    """
    results = ((pickle.dumps(item), True, item) for item in items)
    if compress_large_data:
        results = _cache_compress_pickled_data(results)
    for item in _cache_store_chunks(results, key, expiration):
        yield item


def cache_memoize_iter(key, items_or_callable, expiration=_default_expiration, force_overwrite=False, compress_large_data=True):
    """Memoize an iterable list of items inside the configured cache.

    If the provided list of items is a function, the function must return a
    an iterable object, such as a list or a generator.

    If a generator is provided, directly or through a function, then each
    item will be immediately yielded to the caller as they're retrieved, and
    the cached entries will be built up as the items are processed.

    The data is assumed to be big enough that it must be pickled,
    optionally compressed, and stored as chunks in the cache.

    The result from this function is always a generator. Note that it's
    important that the generator be allowed to continue until completion, or
    the data won't be retrievable from the cache.

    Args:
        expiration (int):
            The expiration time for the key, in seconds.

        force_overwrite (bool):
            If ``True``, the value will always be computed and stored
            regardless of whether it exists in the cache already.

        compress_large_data (bool):
            If ``True``, the data will be zlib-compressed.

    Yields:
        The list of items from the cache or from ``items_or_callable`` if
        uncached.
    """
    results = None
    if not force_overwrite and make_cache_key(key) in cache:
        try:
            results = _cache_iter_large_data(_cache_fetch_large_data(cache, key, compress_large_data), key)
        except Exception as e:
            logger.warning(b'Failed to fetch large data from cache for key %s: %s.' % (
             key, e))
            results = None

    else:
        logger.debug(b'Cache miss for key %s.' % key)
    if results is None:
        if callable(items_or_callable):
            items = items_or_callable()
        else:
            items = items_or_callable
        results = _cache_store_items(cache, key, items, expiration, compress_large_data)
    for item in results:
        yield item

    return


def cache_memoize(key, lookup_callable, expiration=_default_expiration, force_overwrite=False, large_data=False, compress_large_data=True, use_generator=False):
    """Memoize the results of a callable inside the configured cache.

    Args:
        expiration (int):
            The expiration time for the key, in seconds.

        force_overwrite (bool):
            If ``True``, the value will always be computed and stored
            regardless of whether it exists in the cache already.

        large_data (bool):
            If ``True``, the resulting data will be pickled, gzipped, and
            (potentially) split up into megabyte-sized chunks. This is useful
            for very large, computationally intensive hunks of data which we
            don't want to store in a database due to the way things are
            accessed.

        compress_large_data (bool):
            Compresses the data with zlib compression when ``large_data``
            is ``True``.

    Returns:
        The cached data, or the result of ``lookup_callable`` if uncached.
    """
    if large_data:
        results = list(cache_memoize_iter(key, lambda : [
         lookup_callable()], expiration, force_overwrite, compress_large_data))
        assert len(results) == 1
        return results[0]
    else:
        key = make_cache_key(key)
        if not force_overwrite and key in cache:
            return cache.get(key)
        data = lookup_callable()
        if len(data) >= CACHE_CHUNK_SIZE:
            logger.warning(b'Cache data for key "%s" (length %s) may be too big for the cache.' % (
             key, len(data)))
        try:
            cache.set(key, data, expiration)
        except:
            pass

        return data


def make_cache_key(key):
    """Create a cache key guaranteed to avoid conflicts and size limits.

    The cache key will be prefixed by the site's domain, and will be
    changed to an MD5SUM if it's larger than the maximum key size.

    Args:
        key (str): The base key to generate a cache key from.

    Returns:
        str: A cache key suitable for use with the cache backend.
    """
    try:
        site = Site.objects.get_current()
        site_root = getattr(settings, b'SITE_ROOT', None)
        if site_root:
            key = b'%s:%s:%s' % (site.domain, site_root, key)
        else:
            key = b'%s:%s' % (site.domain, key)
    except:
        pass

    key = (b'').join(ch for ch in key if ch not in b' \t\n\r')
    if len(key) > MAX_KEY_SIZE:
        digest = md5(key.encode(b'utf-8')).hexdigest()
        key = key[:MAX_KEY_SIZE - len(digest)] + digest
    key = key.encode(b'utf-8')
    return key