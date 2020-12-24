# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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