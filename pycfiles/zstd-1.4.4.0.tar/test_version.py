# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sergey/workspace-python/github/python-zstd/tests/test_version.py
# Compiled at: 2019-04-28 08:05:59
import os
from tests.base import BaseTestZSTD

class TestZSTD(BaseTestZSTD):

    def setUp(self):
        if os.getenv('ZSTD_EXTERNAL'):
            self.ZSTD_EXTERNAL = True
        self.VERSION = os.getenv('VERSION')
        self.PKG_VERSION = os.getenv('PKG_VERSION')
        v = [ int(n) for n in reversed(self.VERSION.split('.')) ]
        self.VERSION_INT = 0
        i = 0
        for n in v:
            self.VERSION_INT += n * 100 ** i
            i += 1

    def test_module_version(self):
        BaseTestZSTD.helper_version(self)

    def test_library_version(self):
        BaseTestZSTD.helper_zstd_version(self)

    def test_library_version_number(self):
        BaseTestZSTD.helper_zstd_version_number(self)


if __name__ == '__main__':
    unittest.main()