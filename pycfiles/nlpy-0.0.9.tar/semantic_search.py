# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hadoop/nlpy/nlpy/tasks/semantic_search.py
# Compiled at: 2014-11-26 03:42:25
from nlpy.util import NBestList
from nlpy.rep import Word2VecRepresentation
from nlpy.basic import DefaultTokenizer
from nlpy.ex.keyword import DefaultKeywordExtractor
from nlpy.basic import DefaultLemmatizer
from nlpy.basic import DefaultRecaser

class SemanticSearcher(object):

    def __init__(self, tokenizer=None, vec=None):
        self._vec = vec if vec else Word2VecRepresentation()
        self._tokenizer = tokenizer if tokenizer else DefaultTokenizer()
        self._kwex = DefaultKeywordExtractor()
        self._lem = DefaultLemmatizer()
        self._recaser = DefaultRecaser()
        self._data = []

    def load_data(self, data):
        """
        :type data: list of str
        """
        self._data = data

    def search(self, sent):
        """
        :type keywords: list of str
        :return: str
        """
        return self.searchMany(sent, N=1)[0][1]

    def searchMany(self, sent, N=100):
        """
        return n best results
        :param sent: query
        :rtype: list of (str, float)
        """
        nbest = NBestList(N)
        keywords = self._lemmatized_keywords(sent)[:5]
        print keywords
        best_score = 0
        best_sent = ''
        for d in self._data:
            average_score = self.similarity(keywords, d)
            nbest.add(average_score, d)

        if nbest.is_empty():
            nbest.add(0, '')
        return nbest.get()

    def similarity(self, keywords, document):
        keywords_d = self._lemmatized_keywords(document)[:5]
        total_score = 0.0
        count = 0
        for kw_d, wt_d in keywords_d:
            for kw, wt in keywords:
                if kw_d not in self._vec._model.vocab:
                    continue
                total_score += self._vec.similarity(kw_d, kw) * wt * wt_d
                count += 1

        if not count:
            return 0
        average_score = total_score / count
        return average_score

    def _lemmatized_keywords(self, sent):
        keywords = self._kwex.extract_weighted(map(self._recaser.recase, map(self._lem.lemmatize, map(str.lower, self._tokenizer.tokenize(sent)))))
        return keywords

    @staticmethod
    def serve(param):
        global semantic_searcher
        from nlpy.util import external_resource
        from nlpy.util import LineIterator
        import urllib2
        if 'semantic_searcher' not in globals():
            print 'Loading searcher ...'
            data = LineIterator(external_resource('general/elementary_questions.txt'))
            semantic_searcher = SemanticSearcher()
            semantic_searcher.load_data(data)
        caches = set()
        if 'caches' in param:
            caches = set(urllib2.unquote(param['caches']).split(' ||| '))
        print caches
        output = ''
        for _, result in semantic_searcher.searchMany(param['input'].encode('utf-8')):
            if result not in caches:
                output = result
                break

        return {'output': output}