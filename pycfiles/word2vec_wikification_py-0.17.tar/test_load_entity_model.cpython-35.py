# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kensuke-mi/Desktop/analysis_work/wiki_node_disambiguation/tests/test_load_entity_model.py
# Compiled at: 2016-12-02 10:53:35
# Size of source mod 2**32: 1176 bytes
from word2vec_wikification_py import load_entity_model
import unittest, os

class TestLoadEntityModel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.path_model_file = '../bin/entity_vector/entity_vector.model.bin'
        if not os.path.exists(cls.path_model_file):
            cls.path_model_file = cls.path_model_file.replace('../', '')

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_load_entity_model(self):
        model_object = load_entity_model.load_entity_model(path_entity_model=self.path_model_file, is_use_cache=True)
        print(model_object.most_similar('[エン・ジャパン]'))


if __name__ == '__main__':
    unittest.main()