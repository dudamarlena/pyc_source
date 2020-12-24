# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kensuke-mi/Desktop/analysis_work/wiki_node_disambiguation/tests/test_make_lattice.py
# Compiled at: 2016-12-02 10:53:35
# Size of source mod 2**32: 2990 bytes
from word2vec_wikification_py import load_entity_model, make_lattice
from word2vec_wikification_py.models import WikipediaArticleObject, LatticeObject, IndexDictionaryObject
import unittest, os

class TestMakeLatice(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.path_model_file = '../bin/entity_vector/entity_vector.model.bin'
        if not os.path.exists(cls.path_model_file):
            cls.path_model_file = cls.path_model_file.replace('../', '')
        cls.model_object = load_entity_model.load_entity_model(path_entity_model=cls.path_model_file, is_use_cache=True)
        cls.seq_wikipedia_article_object = [
         WikipediaArticleObject(page_title='ヤマハ', candidate_article_name=['[ヤマハ]', '[ヤマハ発動機]']),
         WikipediaArticleObject(page_title='スズキ', candidate_article_name=['[スズキ_(企業)]', '[スズキ_(魚)]']),
         WikipediaArticleObject(page_title='ドゥカティ', candidate_article_name=['[ドゥカティ]'])]

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_make_state_transition_matrix(self):
        """状態tから状態t+1への遷移行列を作成するテスト
        """
        state2index_obj = IndexDictionaryObject(state2index={'row2index': {}, 'column2index': {}}, index2state={})
        transition_edge = make_lattice.make_state_transition_edge(state_t_word_tuple=(0,
                                                                                      '[ヤマハ]'), state_t_plus_word_tuple=(1,
                                                                                                                         '[河合楽器製作所]'), state2index_obj=state2index_obj, entity_vector=self.model_object)
        self.assertTrue(isinstance(transition_edge, tuple))
        self.assertEqual(transition_edge[0].transition_score, self.model_object.similarity('[ヤマハ]', '[河合楽器製作所]'))

    def test_make_state_transition_sequence(self):
        """
        """
        state2index_obj = IndexDictionaryObject(state2index={'row2index': {}, 'column2index': {}}, index2state={})
        make_lattice.make_state_transition_sequence(seq_wiki_article_name=self.seq_wikipedia_article_object, entity_vector_model=self.model_object, state2index_obj=state2index_obj)

    def test_make_lattice_object(self):
        lattice_object = make_lattice.make_lattice_object(seq_wiki_article_name=self.seq_wikipedia_article_object, entity_vector_model=self.model_object, is_use_cache=True)
        self.assertTrue(isinstance(lattice_object, LatticeObject))


if __name__ == '__main__':
    unittest.main()