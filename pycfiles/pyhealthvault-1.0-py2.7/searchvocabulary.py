# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/healthvaultlib/methods/searchvocabulary.py
# Compiled at: 2016-01-05 13:49:28
from lxml import etree
from healthvaultlib.methods.method import Method
from healthvaultlib.objects.vocabularykey import VocabularyKey
from healthvaultlib.objects.vocabularycodeset import VocabularyCodeSet
from healthvaultlib.methods.methodbase import RequestBase, ResponseBase

class SearchVocabularyRequest(RequestBase):
    """
        Attributes:
            search_params   A VocabularySearchParams instance
    """

    def __init__(self, search_params):
        super(SearchVocabularyRequest, self).__init__()
        self.name = 'SearchVocabulary'
        self.version = 1
        self.vocabulary_key = None
        self.text_search_parameters = search_params
        return

    def get_info(self):
        info = etree.Element('info')
        if self.vocabulary_key is not None:
            info.append(self.vocabulary_key.write_xml())
        info.append(self.text_search_parameters.write_xml())
        return info


class SearchVocabularyResponse(ResponseBase):
    """
        The SearchVocabulary response can either contain
        a list of vocabulary keys or a list of vocabulary
        code sets.

        Atrributes:
            vocabulary_key       Array of VocabularyKey
            code_set_result      Array of VocabularyCodeSet
    """

    def __init__(self):
        super(SearchVocabularyResponse, self).__init__()
        self.vocabulary_key = []
        self.code_set_result = []
        self.name = 'SearchVocabulary'
        self.version = 1

    def parse_response(self, response):
        self.parse_info(response)
        for key in self.info.xpath('vocabulary-key'):
            self.vocabulary_key.append(VocabularyKey(key))

        for code_set in self.info.xpath('code-set-result'):
            self.vocabulary_code_set.append(VocabularyCodeSet(code_set))


class SearchVocabulary(Method):
    """
        Searches a vocabulary and retrieves code items that match
        a given search criteria.
    """

    def __init__(self, search_params):
        self.request = SearchVocabularyRequest(search_params)
        self.response = SearchVocabularyResponse()