# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/credstuffer/test/test_proxy.py
# Compiled at: 2019-12-30 19:10:39
# Size of source mod 2**32: 717 bytes
import unittest
from credstuffer import Proxy

class TestProxy(unittest.TestCase):

    def setUp(self) -> None:
        self.proxy = Proxy(timeout_ms=50)

    def test_get(self):
        proxy = self.proxy.get()
        self.assertIsInstance(proxy, str, msg='proxy must be type of string')

    def test_load_proxies(self):
        proxy_list = self.proxy.load_proxies(timeout=50)
        self.assertIsInstance(proxy_list, list, msg='proxy list must be type of list')
        for proxy in proxy_list:
            self.assertIsInstance(proxy, str, msg='proxy must be type of string')

    def tearDown(self) -> None:
        pass


if __name__ == '__main__':
    unittest.main()