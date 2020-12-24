# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-pn36swhz/pip/pip/_vendor/cachecontrol/wrapper.py
# Compiled at: 2020-02-14 17:24:54
# Size of source mod 2**32: 690 bytes
from .adapter import CacheControlAdapter
from .cache import DictCache

def CacheControl(sess, cache=None, cache_etags=True, serializer=None, heuristic=None, controller_class=None, adapter_class=None, cacheable_methods=None):
    cache = DictCache() if cache is None else cache
    adapter_class = adapter_class or CacheControlAdapter
    adapter = adapter_class(cache,
      cache_etags=cache_etags,
      serializer=serializer,
      heuristic=heuristic,
      controller_class=controller_class,
      cacheable_methods=cacheable_methods)
    sess.mount('http://', adapter)
    sess.mount('https://', adapter)
    return sess