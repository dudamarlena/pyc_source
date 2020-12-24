# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/util/future_api_test.py
# Compiled at: 2018-06-15 01:22:48
# Size of source mod 2**32: 1177 bytes
"""Tests for future_api."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import tensorflow as tf
from tensorflow.python.util import future_api

class ExampleParserConfigurationTest(tf.test.TestCase):

    def testBasic(self):
        self.assertFalse(hasattr(tf, 'arg_max'))
        self.assertTrue(hasattr(tf, 'argmax'))


if __name__ == '__main__':
    tf.test.main()