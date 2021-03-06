# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/healthvaultlib/tests/methods/test_searchvocabulary.py
# Compiled at: 2016-01-05 14:35:16
import unittest
from healthvaultlib.tests.testbase import TestBase
from healthvaultlib.objects.vocabularykey import VocabularyKey
from healthvaultlib.methods.searchvocabulary import SearchVocabulary
from healthvaultlib.objects.vocabularysearchparams import VocabularySearchParams

class TestSearchVocabulary(TestBase):

    def test_searchvocabulary_without_key(self):
        search_text = 'International Classification of Diseases'
        params = VocabularySearchParams(search_text)
        params.search_mode = 'Prefix'
        method = SearchVocabulary(params)
        method.execute(self.connection)
        self.assertEqual(len(method.response.code_set_result), 0)
        self.assertNotEqual(len(method.response.vocabulary_key), 0)
        self.assertTrue(search_text in method.response.vocabulary_key[0].name or search_text in method.response.vocabulary_key[0].description)

    @unittest.skip('Something wrong with HV method, I suppose')
    def test_searchvocabulary_with_key(self):
        thing = VocabularyKey()
        thing.name = 'thing-types'
        thing.family = 'wc'
        thing.version = '1'
        search_text = 'e'
        params = VocabularySearchParams(search_text)
        params.search_mode = 'Contains'
        method = SearchVocabulary(params)
        method.request.vocabulary_key = thing
        method.execute(self.connection)
        self.assertNotEqual(len(method.response.code_set_result), 0)
        self.assertEqual(len(method.response.vocabulary_key), 0)
        self.assertTrue(search_text in method.response.code_set_result[0].name or search_text in method.response.code_set_result[0].description)