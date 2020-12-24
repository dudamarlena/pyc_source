# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/utils/label_map_util_test.py
# Compiled at: 2018-06-15 01:29:01
# Size of source mod 2**32: 4725 bytes
"""Tests for object_detection.utils.label_map_util."""
import os, tensorflow as tf
from google.protobuf import text_format
from object_detection.protos import string_int_label_map_pb2
from object_detection.utils import label_map_util

class LabelMapUtilTest(tf.test.TestCase):

    def _generate_label_map(self, num_classes):
        label_map_proto = string_int_label_map_pb2.StringIntLabelMap()
        for i in range(1, num_classes + 1):
            item = label_map_proto.item.add()
            item.id = i
            item.name = 'label_' + str(i)
            item.display_name = str(i)

        return label_map_proto

    def test_get_label_map_dict(self):
        label_map_string = "\n      item {\n        id:2\n        name:'cat'\n      }\n      item {\n        id:1\n        name:'dog'\n      }\n    "
        label_map_path = os.path.join(self.get_temp_dir(), 'label_map.pbtxt')
        with tf.gfile.Open(label_map_path, 'wb') as (f):
            f.write(label_map_string)
        label_map_dict = label_map_util.get_label_map_dict(label_map_path)
        self.assertEqual(label_map_dict['dog'], 1)
        self.assertEqual(label_map_dict['cat'], 2)

    def test_load_bad_label_map(self):
        label_map_string = "\n      item {\n        id:0\n        name:'class that should not be indexed at zero'\n      }\n      item {\n        id:2\n        name:'cat'\n      }\n      item {\n        id:1\n        name:'dog'\n      }\n    "
        label_map_path = os.path.join(self.get_temp_dir(), 'label_map.pbtxt')
        with tf.gfile.Open(label_map_path, 'wb') as (f):
            f.write(label_map_string)
        with self.assertRaises(ValueError):
            label_map_util.load_labelmap(label_map_path)

    def test_keep_categories_with_unique_id(self):
        label_map_proto = string_int_label_map_pb2.StringIntLabelMap()
        label_map_string = "\n      item {\n        id:2\n        name:'cat'\n      }\n      item {\n        id:1\n        name:'child'\n      }\n      item {\n        id:1\n        name:'person'\n      }\n      item {\n        id:1\n        name:'n00007846'\n      }\n    "
        text_format.Merge(label_map_string, label_map_proto)
        categories = label_map_util.convert_label_map_to_categories(label_map_proto, max_num_classes=3)
        self.assertListEqual([
         {'id': 2, 
          'name': 'cat'},
         {'id': 1, 
          'name': 'child'}], categories)

    def test_convert_label_map_to_categories_no_label_map(self):
        categories = label_map_util.convert_label_map_to_categories(None, max_num_classes=3)
        expected_categories_list = [
         {'name': 'category_1', 
          'id': 1},
         {'name': 'category_2', 
          'id': 2},
         {'name': 'category_3', 
          'id': 3}]
        self.assertListEqual(expected_categories_list, categories)

    def test_convert_label_map_to_coco_categories(self):
        label_map_proto = self._generate_label_map(num_classes=4)
        categories = label_map_util.convert_label_map_to_categories(label_map_proto, max_num_classes=3)
        expected_categories_list = [
         {'name': '1', 
          'id': 1},
         {'name': '2', 
          'id': 2},
         {'name': '3', 
          'id': 3}]
        self.assertListEqual(expected_categories_list, categories)

    def test_convert_label_map_to_coco_categories_with_few_classes(self):
        label_map_proto = self._generate_label_map(num_classes=4)
        cat_no_offset = label_map_util.convert_label_map_to_categories(label_map_proto, max_num_classes=2)
        expected_categories_list = [
         {'name': '1', 
          'id': 1},
         {'name': '2', 
          'id': 2}]
        self.assertListEqual(expected_categories_list, cat_no_offset)

    def test_create_category_index(self):
        categories = [{'name': '1',  'id': 1}, {'name': '2',  'id': 2}]
        category_index = label_map_util.create_category_index(categories)
        self.assertDictEqual({1: {'name': '1', 
             'id': 1}, 
         2: {'name': '2', 
             'id': 2}}, category_index)


if __name__ == '__main__':
    tf.test.main()