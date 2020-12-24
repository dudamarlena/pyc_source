# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/imagehash/tests/test_average_hash.py
# Compiled at: 2017-12-06 18:12:41
from __future__ import absolute_import, division, print_function
from PIL import Image
import unittest, imagehash, imagehash.tests as tests

class Test(tests.TestImageHash):

    def setUp(self):
        self.image = self.get_data_image()
        self.func = imagehash.average_hash

    def test_average_hash(self):
        self.check_hash_algorithm(self.func, self.image)

    def test_average_hash_length(self):
        self.check_hash_length(self.func, self.image)

    def test_average_hash_stored(self):
        self.check_hash_stored(self.func, self.image)

    def test_average_hash_size(self):
        self.check_hash_size(self.func, self.image)


if __name__ == '__main__':
    unittest.main()