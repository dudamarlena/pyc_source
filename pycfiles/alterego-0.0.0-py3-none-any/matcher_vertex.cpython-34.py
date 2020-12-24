# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/alteraparser/syntaxgraph/matcher_vertex.py
# Compiled at: 2015-12-30 04:57:43
# Size of source mod 2**32: 952 bytes
from .vertex import Vertex, VertexCategory

class MatcherVertex(Vertex):

    def __init__(self, chars=[], negated=False):
        Vertex.__init__(self, VertexCategory.MATCHER)
        self._MatcherVertex__chars = set(chars)
        self._MatcherVertex__negated = negated

    def matches(self, ch):
        if not self._MatcherVertex__negated:
            return ch in self._MatcherVertex__chars
        else:
            return ch not in self._MatcherVertex__chars

    def negate(self, neg=True):
        self._MatcherVertex__negated = neg
        return self

    def add(self, ch):
        self._MatcherVertex__chars.append(ch)
        return self

    def _on_clone_creation(self, original):
        Vertex._on_clone_creation(self, original)
        self._MatcherVertex__chars = set(original._MatcherVertex__chars)
        self._MatcherVertex__negated = original._MatcherVertex__negated

    def __str__(self):
        chars = '[' + ','.join(self._MatcherVertex__chars) + ']'
        if self._MatcherVertex__negated:
            return 'MATCH: NOT {}'.format(chars)
        else:
            return 'MATCH: {}'.format(chars)