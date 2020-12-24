# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/cache_it/test_init_cache.py
# Compiled at: 2014-06-17 10:25:22
from nose.tools import raises
from cache_it import cache_it, init_cache, cache
import switchcache

def setup():
    init_cache(['invalidhost:12345'])


@cache_it(prefix='PREFIX', ignore_exception=False)
def get_item_with_exception(key):
    return 'value'


@cache_it(prefix='PREFIX', ignore_exception=True)
def get_item_no_exception(key):
    return 'value'


@raises(Exception)
def test_with_exception():
    get_item_with_exception('hoge')


@switchcache.no_cache
def test_no_exception():
    assert get_item_no_exception('hoge') == 'value'