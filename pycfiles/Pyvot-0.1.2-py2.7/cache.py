# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build-py2\bdist.egg\xl\cache.py
# Compiled at: 2011-11-21 15:27:19
"""Cache layer

Pyvot must assume that the contents of an Excel workbook can change at any time, due to interactive manipulation 
or other external influences. Living out of process, this can be a performance catastrophe. We use a cache when
possible, on the assumption that Excel doesn't change during any single call into to the Pyvot user API.

This module provides the :func:`@cache_result` decorator which adds caching to a function or property,
an :func:`@enable_caching` decorator for enabling the (off by default) cache for the duration of a function call, and the
CacheManager, for non-decorator cache control including invalidation."""
import contextlib, functools

def enable_caching(f):
    """Decorator which enables caching within the wrapped function. Caching is enabled
    until the function exits; i.e. functions called directly or indirectly will also have
    caching enabled."""
    import functools

    @functools.wraps(f)
    def _wrapped(*args, **kwargs):
        with CacheManager.caching_enabled():
            return f(*args, **kwargs)

    return _wrapped


class _ResultCachingDescriptor(object):
    """Decorator class for caching the results of method calls / read-only properties. The cache is controlled
    by the state of the singleton CacheManager. While caching is enabled, the wrapped function / property
    is called only once per unique set of arguments, and the return value is stored to satisfy future
    calls with those same arguments. When caching is disabled, all cached values are cleared, and
    the wrapped function is always called.

    This decorator may only be applied to a method or property within a class. A separate cache is maintained *per instance*; 
    although argument sets are typically compared for value equality, two equal instances still have separate caches.
    
    Cache statistics are available via the 'stats' attribute (unless wrapping a property):
        
        instance_a.cached_method -> CacheSite instance
        instance_a.cached_method.stats.hits -> # of cache hits (similarly for misses)
        instance_b.cached_method -> Different CacheSite instance

    This information is summarized by CacheManager.cache_info(), in which the per-instance stats are aggregated by class"""

    def __init__(self, f, as_property=False):
        assert callable(f) or isinstance(f, property)
        self._wrapped = f
        self._wrapping_property = isinstance(f, property)
        self._update_wrapper(self)

    def _update_wrapper(self, o):
        """Updates the given object with __name__, __doc__, etc. from the wrapped thing.
        Just like functools.update_wrapper, but handles the case where we are wrapping a property"""
        wrapped_func = self._wrapped.fget if self._wrapping_property else self._wrapped
        functools.update_wrapper(o, wrapped_func)

    def __get__(self, instance, owning_class=None):
        if instance is None:
            return self
        else:
            try:
                instance_sites = instance.__cache_sites
            except AttributeError:
                instance_sites = instance.__cache_sites = {}

            if self not in instance_sites:
                if self._wrapping_property:

                    def _wrapped_with_instance():
                        return self._wrapped.__get__(instance, owning_class)

                    site_name = '%s (instance of %s at %x)' % (repr(self._wrapped.fget), str(owning_class), id(instance))
                else:

                    def _wrapped_with_instance(*args, **kwargs):
                        return self._wrapped(instance, *args, **kwargs)

                    site_name = '%s (instance of %s at %x)' % (repr(self._wrapped), str(owning_class), id(instance))
                wrapped_key = (self._wrapping_property or self)._wrapped if 1 else self._wrapped.fget
                self._update_wrapper(_wrapped_with_instance)
                instance_sites[self] = CacheManager.create_cache_site(_wrapped_with_instance, site_name, site_group_key=(
                 wrapped_key, type(instance)))
            if self._wrapping_property:
                return instance_sites[self]()
            return instance_sites[self]
            return

    def __call__(self, *args, **kwargs):
        raise TypeError('_ResultCachingDescriptor is not callable. Only methods within a class (not normal functions) may be cached')


cache_result = _ResultCachingDescriptor

class CacheSite(object):
    """Represents a single cache of arguments -> results.
    Note that there can be multiple cache sites per @cache_result-wrapped method;
    each instance with the caching method uses a separate cache site"""

    def __init__(self, source, site_name=None):
        assert callable(source)
        if site_name is None:
            site_name = repr(self)
        self.source = source
        self.stats = CacheSiteStats()
        self.site_name = site_name
        self._cached = {}
        functools.update_wrapper(self, source)
        return

    def clear(self):
        self._cached.clear()

    def _key(self, *args, **kwargs):
        return (
         args, tuple(sorted(kwargs.items())))

    def get(self, *args, **kwargs):
        if not CacheManager.is_caching_enabled:
            self.stats.uncached_misses += 1
            return self.source(*args, **kwargs)
        else:
            k = self._key(*args, **kwargs)
            if k in self._cached:
                self.stats.hits += 1
                return self._cached[k]
            self.stats.misses += 1
            v = self.source(*args, **kwargs)
            self._cached[k] = v
            return v

    __call__ = get


class CacheSiteStats(object):
    """Container for :attr:`hits`, :attr:`misses`, and :attr:`uncached_misses`
    (misses that occurred with cachind disabled). Accessed as :attr:`CacheSite.stats`"""

    def __init__(self):
        self.hits = self.misses = self.uncached_misses = 0


class CacheManager_class(object):
    """Singleton manager for the program's CacheSites (created through use of @:func:`cache_result`)
    Cache state is dynamically scoped on the stack by use of a context manager::

        with CacheManager.caching_enabled():
            do_stuff()

    Within that context, all @cache_result decorators are enabled and may store / return cached values
    Cached values are deleted when the context is exited. 
    
    The context may be safely nested."""

    def __init__(self):
        self._cache_level = 0
        self._site_weakrefs = set()
        self._site_stats = {}
        self._iterating_site_weakrefs = False

    @contextlib.contextmanager
    def caching_enabled(self):
        """Returns an object implementing the context-manager protocol. Within the context,
        caching is enabled (this is a context-manager version of the `@enable_caching` decorator).
        
        Cache activation may be nested; there is no harm in enabling caching before calling a function
        which does the same::
        
            with xl.CacheManager.caching_enabled():
                with xl.CacheManager.caching_enabled():
                    assert xl.CacheManager.is_caching_enabled()
                assert xl.CacheManager.is_caching_enabled()
            assert not xl.CacheManager.is_caching_enabled()"""
        self._increment_cache_level()
        try:
            yield
        finally:
            self._decrement_cache_level()

    @contextlib.contextmanager
    def caching_disabled(self):
        """Returns an object implementing the context-manager protocol. Within the context, caching is
        disabled. When exiting the context, the cache-enable state (incl. nesting level) is restored to its
        previous value. Entering the context immediately invalidates all cache sites
        
        ::

            with xl.CacheManager.caching_enabled():
                with xl.CacheManager.caching_disabled():
                    assert not xl.CacheManager.is_caching_enabled()
                assert xl.CacheManager.is_caching_enabled()"""
        old_level = self._cache_level
        if old_level > 0:
            self._cache_level = 0
            self.invalidate_all_caches()
        try:
            yield
        finally:
            self._cache_level = old_level

    @property
    def is_caching_enabled(self):
        return self._cache_level > 0

    def _increment_cache_level(self):
        self._cache_level += 1

    def _decrement_cache_level(self):
        assert self._cache_level > 0
        self._cache_level -= 1
        if self._cache_level == 0:
            self.invalidate_all_caches()

    def create_cache_site(self, source, site_name, site_group_key):
        """Creates a CacheSite instanced, managed by this CacheManager.
        The manager keeps a weak reference to the site ; the lifetime of the
        cache is controlled by the caller
        
        The site_group_key specifies the key on which to aggregate hit / miss stats in cache_info()
        Note that a reference to site_group_key will continue to be held by the CacheManager, so take
        care to select keys that are small in size, or wouldn't be garbage collected anyway (i.e. a module-level class)"""
        import weakref
        cs = CacheSite(source=source, site_name=site_name)
        stats = cs.stats
        cs_weak = weakref.ref(cs, self._on_site_unreferenced)
        self._site_weakrefs.add(cs_weak)
        self._site_stats.setdefault(site_group_key, []).append(stats)
        return cs

    def cache_info(self):
        """Returns a tuple (site group key, group size, hits, misses, uncached misses) per cache site group.
        (uncached misses refers to those misses that occurred without caching enabled (see CacheManager.is_caching_enabled)
        A cache site group is an aggregation of cache sites that are considered meaningfully related,
        with regards to performance counters.
        
        For example, though a method on a class has a cache site per _instance_, all instance sites
        of a method are joined to the same site group."""
        for site_group_key, group_stats in self._site_stats.iteritems():
            yield (
             site_group_key, len(group_stats),
             sum([ stat.hits for stat in group_stats ]),
             sum([ stat.misses for stat in group_stats ]),
             sum([ stat.uncached_misses for stat in group_stats ]))

    def invalidate_all_caches(self):
        """Invalidates cache sites program-wide. This method should be called whenever the Excel COM API is used to
        modify a workbook (for example, it is called by :meth:`xl.range.Range.set`).

        Alternatively, one can use :meth:`caching_disabled`, since it invalidates caches on context entry."""
        for site in self._iter_site_refs():
            site.clear()

    def _iter_site_refs(self):
        old_iter_state = self._iterating_site_weakrefs
        self._iterating_site_weakrefs = True
        try:
            for site_weakref in self._site_weakrefs:
                site = site_weakref()
                if site is not None:
                    yield site

            to_discard = set()
            for site_weakref in self._site_weakrefs:
                if site_weakref() is None:
                    to_discard.add(site_weakref)

            self._site_weakrefs -= to_discard
        finally:
            self._iterating_site_weakrefs = False

        return

    def _on_site_unreferenced(self, site_weakref):
        if not self._iterating_site_weakrefs:
            self._site_weakrefs.discard(site_weakref)


CacheManager = CacheManager_class()