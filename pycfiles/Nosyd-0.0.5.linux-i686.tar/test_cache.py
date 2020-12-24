# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.6/dist-packages/nosyd/tests/test_cache.py
# Compiled at: 2009-10-08 08:42:29
from nosyd.nosyd import *
from nosyd.cache import *

class CountCalls:

    def __init__(self):
        self.my_cache = {}
        self.calls = 0

    @MWT(timeout=0.2, cache_attr_name='my_cache')
    def cachedCall(self):
        self.calls += 1


class TestNosyd:

    def test_cache(self):
        cc = CountCalls()
        assert cc.calls == 0
        assert len(cc.my_cache) == 0
        cc.cachedCall()
        assert cc.calls == 1
        assert len(cc.my_cache) == 1
        cc.cachedCall()
        assert cc.calls == 1
        assert len(cc.my_cache) == 1
        cc.my_cache.clear()
        assert len(cc.my_cache) == 0
        cc.cachedCall()
        assert cc.calls == 2
        assert len(cc.my_cache) == 1
        time.sleep(0.5)
        MWT().collect()
        assert len(cc.my_cache) == 0
        cc.cachedCall()
        assert cc.calls == 3
        assert len(cc.my_cache) == 1