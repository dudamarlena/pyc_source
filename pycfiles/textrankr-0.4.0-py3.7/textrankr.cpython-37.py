# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/textrankr/textrankr.py
# Compiled at: 2019-07-20 08:55:11
# Size of source mod 2**32: 1850 bytes
from re import split
from networkx import Graph
from networkx import pagerank
from itertools import combinations
from .sentence import Sentence

class TextRank(object):

    def __init__(self, text):
        self.text = text.strip()
        self.build()

    def build(self):
        self._build_sentences()
        self._build_graph()
        self.pageranks = pagerank((self.graph), weight='weight')
        self.reordered = sorted((self.pageranks), key=(self.pageranks.get), reverse=True)

    def _build_sentences(self):
        dup = {}
        candidates = split('(?:(?<=[^0-9])\\.|\\n)', self.text)
        self.sentences = []
        index = 0
        for candidate in candidates:
            while not len(candidate) or candidate[(-1)] == '.' or candidate[(-1)] == ' ':
                candidate = candidate.strip(' ').strip('.')

            if len(candidate) and candidate not in dup:
                dup[candidate] = True
                self.sentences.append(Sentence(candidate + '.', index))
                index += 1

        del dup
        del candidates

    def _build_graph(self):
        self.graph = Graph()
        self.graph.add_nodes_from(self.sentences)
        for sent1, sent2 in combinations(self.sentences, 2):
            weight = self._jaccard(sent1, sent2)
            if weight:
                self.graph.add_edge(sent1, sent2, weight=weight)

    def _jaccard(self, sent1, sent2):
        p = sum((sent1.bow & sent2.bow).values())
        q = sum((sent1.bow | sent2.bow).values())
        if q:
            return p / q
        return 0

    def summarize(self, count=3, verbose=True):
        results = sorted((self.reordered[:count]), key=(lambda sentence: sentence.index))
        results = [result.text for result in results]
        if verbose:
            return '\n'.join(results)
        return results