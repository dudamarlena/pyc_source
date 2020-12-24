# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/khan/tests/test_testing.py
# Compiled at: 2010-05-12 10:25:54
from khan.utils.testing import *

class TestDictTester(DictTester, TestCase):

    def setUp(self):
        self.store = dict(map(lambda x: (str(x), str(x)), range(100)))
        super(TestDictTester, self).setUp()


if __name__ == '__main__':
    unittest.main()