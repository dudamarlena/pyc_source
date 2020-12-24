# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ultracache/utils.py
# Compiled at: 2019-12-31 02:49:50
# Size of source mod 2**32: 9299 bytes
import hashlib
from collections import OrderedDict
from django.core.cache import cache
from django.conf import settings
from django.http.cookie import SimpleCookie
from ultracache import _thread_locals
try:
    MAX_SIZE = settings.ULTRACACHE['max-registry-value-size']
except (AttributeError, KeyError):
    MAX_SIZE = 1000000

try:
    CONSIDER_HEADERS = [header.lower() for header in settings.ULTRACACHE['consider-headers']]
except (AttributeError, KeyError):
    CONSIDER_HEADERS = []

try:
    CONSIDER_COOKIES = [cookie.lower() for cookie in settings.ULTRACACHE['consider-cookies']]
except (AttributeError, KeyError):
    CONSIDER_COOKIES = []

if CONSIDER_COOKIES:
    if 'cookie' in CONSIDER_HEADERS:
        raise RuntimeError('consider-cookies has a value but cookie is also present in consider-headers')

def reduce_list_size(li):
    """Return two lists
        - the last N items of li whose total size is less than MAX_SIZE
        - the rest of the original list li
    """
    size = len(repr(li))
    keep = li
    toss = []
    n = len(li)
    decrement_by = max(n / 10, 10)
    while size >= MAX_SIZE and n > 0:
        n -= decrement_by
        toss = li[:-n]
        keep = li[-n:]
        size = len(repr(keep))

    return (
     keep, toss)


def cache_meta(recorder, cache_key, start_index=0, request=None):
    """Inspect request for objects in _ultracache and set appropriate entries
    in Django's cache."""
    path = None
    if request is not None:
        path = request.get_full_path()
        headers = OrderedDict()
        for k, v in sorted(request.META.items()):
            if k == 'HTTP_COOKIE' and CONSIDER_COOKIES:
                cookie = SimpleCookie()
                cookie.load(v)
                headers['cookie'] = '; '.join(['%s=%s' % (k, morsel.value) for k, morsel in sorted(cookie.items()) if k in CONSIDER_COOKIES])
            else:
                if k.startswith('HTTP_'):
                    k = k[5:].replace('_', '-').lower()
                    if k in CONSIDER_HEADERS:
                        headers[k] = v

    to_set_get_keys = []
    to_set_paths_get_keys = []
    to_set_content_types_get_keys = []
    to_set_content_types_paths_get_keys = []
    to_set = {}
    to_set_paths = {}
    to_set_content_types = {}
    to_set_content_types_paths = {}
    to_delete = []
    to_set_objects = []
    for ctid, obj_pk in recorder[start_index:]:
        key = 'ucache-%s-%s' % (ctid, obj_pk)
        if key not in to_set_get_keys:
            to_set_get_keys.append(key)
        key = 'ucache-pth-%s-%s' % (ctid, obj_pk)
        if key not in to_set_paths_get_keys:
            to_set_paths_get_keys.append(key)
        key = 'ucache-ct-%s' % ctid
        if key not in to_set_content_types_get_keys:
            to_set_content_types_get_keys.append(key)
        key = 'ucache-ct-pth-%s' % ctid
        if key not in to_set_content_types_paths_get_keys:
            to_set_content_types_paths_get_keys.append(key)
        tu = (
         ctid, obj_pk)
        if tu not in to_set_objects:
            to_set_objects.append(tu)

    di = cache.get_many(to_set_get_keys)
    for key in to_set_get_keys:
        v = di.get(key, None)
        keep = []
        if v is not None:
            keep, toss = reduce_list_size(v)
            if toss:
                to_set[key] = keep
                to_delete.extend(toss)
        if cache_key not in keep:
            if key not in to_set:
                to_set[key] = keep
            to_set[key] = to_set[key] + [cache_key]

    if to_set == di:
        to_set = {}
    di = cache.get_many(to_set_paths_get_keys)
    for key in to_set_paths_get_keys:
        v = di.get(key, None)
        keep = []
        if v is not None:
            keep, toss = reduce_list_size(v)
            if toss:
                to_set_paths[key] = keep
        if path is not None:
            if [
             path, headers] not in keep:
                if key not in to_set_paths:
                    to_set_paths[key] = keep
            to_set_paths[key] = to_set_paths[key] + [[path, headers]]

    if to_set_paths == di:
        to_set_paths = {}
    di = cache.get_many(to_set_content_types_get_keys)
    for key in to_set_content_types_get_keys:
        v = di.get(key, None)
        keep = []
        if v is not None:
            keep, toss = reduce_list_size(v)
            if toss:
                to_set_content_types[key] = keep
                to_delete.extend(toss)
        if cache_key not in keep:
            if key not in to_set_content_types:
                to_set_content_types[key] = keep
            to_set_content_types[key] = to_set_content_types[key] + [cache_key]

    if to_set_content_types == di:
        to_set_content_types = {}
    di = cache.get_many(to_set_content_types_paths_get_keys)
    for key in to_set_content_types_paths_get_keys:
        v = di.get(key, None)
        keep = []
        if v is not None:
            keep, toss = reduce_list_size(v)
            if toss:
                to_set_content_types_paths[key] = keep
        if path is not None:
            if [
             path, headers] not in keep:
                if key not in to_set_content_types_paths:
                    to_set_content_types_paths[key] = keep
            to_set_content_types_paths[key] = to_set_content_types_paths[key] + [
             [
              path, headers]]

    if to_set_content_types_paths == di:
        to_set_content_types_paths = {}
    if to_delete:
        try:
            cache.delete_many(to_delete)
        except NotImplementedError:
            for k in to_delete:
                cache.delete(k)

    di = {}
    di.update(to_set)
    del to_set
    di.update(to_set_paths)
    del to_set_paths
    di.update(to_set_content_types)
    del to_set_content_types
    di.update(to_set_content_types_paths)
    del to_set_content_types_paths
    if to_set_objects:
        di[cache_key + '-objs'] = to_set_objects
    if di:
        try:
            cache.set_many(di, 86400)
        except NotImplementedError:
            for k, v in di.items():
                cache.set(k, v, 86400)


def get_current_site_pk(request):
    """Seemingly pointless function is so calling code doesn't have to worry
    about the import issues between Django 1.6 and later."""
    from django.contrib.sites.models import Site
    try:
        from django.contrib.sites.shortcuts import get_current_site
    except ImportError:
        from django.contrib.sites.models import get_current_site

    return get_current_site(request).pk


class EmptyMarker:
    pass


empty_marker_1 = EmptyMarker()
empty_marker_2 = EmptyMarker()

class Ultracache:
    __doc__ = 'Cache arbitrary pieces of Python code.\n    '

    def __init__(self, timeout, name, *params, request=None):
        self.timeout = timeout
        self.request = request
        self._cached = empty_marker_1
        s = ':'.join([name] + [str(p) for p in params])
        hashed = hashlib.md5(s.encode('utf-8')).hexdigest()
        self.cache_key = 'ucache-%s' % hashed
        self.start_index = len(_thread_locals.ultracache_recorder)
        self.used = False

    @property
    def cached(self):
        if self._cached is empty_marker_1:
            self._cached = cache.get(self.cache_key, empty_marker_2)
        return self._cached

    def __bool__(self):
        return self.cached is not empty_marker_2

    def cache(self, value):
        if self.used:
            raise RuntimeError('The cache method may only be called once per Ultracache object.')
        cache.set(self.cache_key, value, self.timeout)
        cache_meta((_thread_locals.ultracache_recorder),
          (self.cache_key),
          start_index=(self.start_index),
          request=(self.request))
        self.used = True