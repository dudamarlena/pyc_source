# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/travis/build/tgsmith61591/pyramid/pyramid/_config.py
# Compiled at: 2018-11-02 11:39:14
from __future__ import absolute_import
import os
from os.path import expanduser
import warnings
PYRAMID_ARIMA_CACHE = os.environ.get('PYRAMID_ARIMA_CACHE', expanduser('~/.pyramid-arima-cache'))
PICKLE_HASH_PATTERN = '%s-%s-%i.pmdpkl'
cwb = os.environ.get('PYRAMID_ARIMA_CACHE_WARN_SIZE', 100000000.0)
try:
    CACHE_WARN_BYTES = int(cwb)
except ValueError:
    warnings.warn(('The value of PYRAMID_ARIMA_CACHE_WARN_SIZE should be an integer, but got "{cache_val}". Defaulting to 1e8.').format(cache_val=cwb))
    CACHE_WARN_BYTES = 100000000.0

def _warn_for_cache_size():
    """Warn for a cache size that is too large.

    This is called on the initial import and warns if the size of the cached
    statsmodels TS objects exceeds the CACHE_WARN_BYTES value.
    """
    from os.path import join, getsize, isfile
    try:
        cache_size = sum(getsize(join(PYRAMID_ARIMA_CACHE, f)) for f in os.listdir(PYRAMID_ARIMA_CACHE) if isfile(join(PYRAMID_ARIMA_CACHE, f)))
    except OSError as ose:
        if ose.errno != 2:
            raise

    if cache_size > CACHE_WARN_BYTES:
        warnings.warn(("The Pyramid cache ({cache_loc}) has grown to {nbytes:,} bytes. Consider cleaning out old ARIMA models or increasing the max cache bytes with 'PYRAMID_ARIMA_CACHE_WARN_SIZE' (currently {current_max:,} bytes) to avoid this warning in the future.").format(cache_loc=PYRAMID_ARIMA_CACHE, nbytes=cache_size, current_max=int(CACHE_WARN_BYTES)), UserWarning)