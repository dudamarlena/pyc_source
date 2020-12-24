# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bauble/test/test_utils.py
# Compiled at: 2016-10-03 09:39:22
import bauble.utils as utils
from unittest import TestCase

class Utils(TestCase):

    def test_topological_sort_total(self):
        self.assertEqual(utils.topological_sort([1, 2, 3], [(2, 1), (3, 2)]), [3, 2, 1])

    def test_topological_sort_partial(self):
        self.assertEqual(utils.topological_sort([1, 2, 3, 4], [(2, 1)]), [4, 3, 2, 1])

    def test_topological_sort_loop(self):
        self.assertEqual(utils.topological_sort([1, 2], [(2, 1), (1, 2)]), None)
        return


class CacheTest(TestCase):

    def test_create_store_retrieve(self):
        from bauble.utils import Cache
        from functools import partial
        invoked = []

        def getter(x):
            invoked.append(x)
            return x

        cache = Cache(2)
        v = cache.get(1, partial(getter, 1))
        self.assertEquals(v, 1)
        self.assertEquals(invoked, [1])
        v = cache.get(1, partial(getter, 1))
        self.assertEquals(v, 1)
        self.assertEquals(invoked, [1])

    def test_respect_size(self):
        from bauble.utils import Cache
        from functools import partial
        invoked = []

        def getter(x):
            invoked.append(x)
            return x

        cache = Cache(2)
        cache.get(1, partial(getter, 1))
        cache.get(2, partial(getter, 2))
        cache.get(3, partial(getter, 3))
        cache.get(4, partial(getter, 4))
        self.assertEquals(invoked, [1, 2, 3, 4])
        self.assertEquals(sorted(cache.storage.keys()), [3, 4])

    def test_respect_timing(self):
        from bauble.utils import Cache
        from functools import partial
        invoked = []

        def getter(x):
            invoked.append(x)
            return x

        cache = Cache(2)
        cache.get(1, partial(getter, 1))
        cache.get(2, partial(getter, 2))
        cache.get(1, partial(getter, 1))
        cache.get(3, partial(getter, 3))
        cache.get(1, partial(getter, 1))
        cache.get(4, partial(getter, 4))
        self.assertEquals(invoked, [1, 2, 3, 4])
        self.assertEquals(sorted(cache.storage.keys()), [1, 4])

    def test_cache_on_hit(self):
        from bauble.utils import Cache
        from functools import partial
        invoked = []

        def getter(x):
            return x

        cache = Cache(2)
        cache.get(1, partial(getter, 1), on_hit=invoked.append)
        cache.get(1, partial(getter, 1), on_hit=invoked.append)
        cache.get(2, partial(getter, 2), on_hit=invoked.append)
        cache.get(1, partial(getter, 1), on_hit=invoked.append)
        cache.get(3, partial(getter, 3), on_hit=invoked.append)
        cache.get(1, partial(getter, 1), on_hit=invoked.append)
        cache.get(4, partial(getter, 4), on_hit=invoked.append)
        self.assertEquals(invoked, [1, 1, 1])
        self.assertEquals(sorted(cache.storage.keys()), [1, 4])


class GlobalFuncs(TestCase):

    def test_safe_int_valid(self):
        self.assertEquals(utils.safe_int('123'), 123)

    def test_safe_int_valid_not(self):
        self.assertEquals(utils.safe_int('123.2'), 0)

    def test_safe_numeric_valid(self):
        self.assertEquals(utils.safe_numeric('123'), 123)

    def test_safe_numeric_valid_decimal(self):
        self.assertEquals(utils.safe_numeric('123.2'), 123.2)

    def test_safe_numeric_valid_not(self):
        self.assertEquals(utils.safe_numeric('123a.2'), 0)