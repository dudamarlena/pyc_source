# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/utils/dataset_util_test.py
# Compiled at: 2018-06-15 01:29:00
# Size of source mod 2**32: 1296 bytes
"""Tests for object_detection.utils.dataset_util."""
import os, tensorflow as tf
from object_detection.utils import dataset_util

class DatasetUtilTest(tf.test.TestCase):

    def test_read_examples_list(self):
        example_list_data = 'example1 1\nexample2 2'
        example_list_path = os.path.join(self.get_temp_dir(), 'examples.txt')
        with tf.gfile.Open(example_list_path, 'wb') as (f):
            f.write(example_list_data)
        examples = dataset_util.read_examples_list(example_list_path)
        self.assertListEqual(['example1', 'example2'], examples)


if __name__ == '__main__':
    tf.test.main()