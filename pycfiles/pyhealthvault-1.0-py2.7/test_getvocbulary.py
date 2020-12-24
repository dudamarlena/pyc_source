# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/healthvaultlib/tests/methods/test_getvocbulary.py
# Compiled at: 2016-01-05 14:35:17
from healthvaultlib.tests.testbase import TestBase
from healthvaultlib.methods.getvocabulary import GetVocabulary
from healthvaultlib.objects.vocabularyparameters import VocabularyParameters
from healthvaultlib.objects.vocabularykey import VocabularyKey

class TestGetVocabulary(TestBase):

    def test_getvocabulary_keys(self):
        method = GetVocabulary()
        method.execute(self.connection)
        self.assertEqual(len(method.response.vocabulary_code_set), 0)
        self.assertNotEqual(len(method.response.vocabulary_key), 0)

    def test_getvocabulary(self):
        method = GetVocabulary()
        thing = VocabularyKey()
        thing.name = 'thing-types'
        thing.family = 'wc'
        thing.version = '1'
        param = VocabularyParameters([thing])
        method.request.vocabulary_parameters = param
        method.execute(self.connection)
        self.assertNotEqual(len(method.response.vocabulary_code_set), 0)
        self.assertNotEqual(len(method.response.vocabulary_code_set[0].code_item), 0)
        self.assertEqual(len(method.response.vocabulary_key), 0)