# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/tests/test_api_guess.py
# Compiled at: 2013-12-18 08:08:21
from framework import DoubanClientTestBase, main

class TestApiGuess(DoubanClientTestBase):

    def setUp(self):
        super(TestApiGuess, self).setUp()
        self.user_id = '40774605'


if __name__ == '__main__':
    main()