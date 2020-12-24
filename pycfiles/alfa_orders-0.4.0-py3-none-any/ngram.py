# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/alfanous/Support/whoosh/qparser/ngram.py
# Compiled at: 2015-06-30 06:52:38
from alfanous.Support.whoosh.analysis import NgramAnalyzer
from alfanous.Support.whoosh.query import *

class SimpleNgramParser(object):
    """A simple parser that only allows searching a single Ngram field. Breaks
    the input text into grams. It can either discard grams containing spaces,
    or compose them as optional clauses to the query.
    """
    __inittypes__ = dict(fieldname=str, minchars=int, maxchars=int, discardspaces=bool, analyzerclass=type)

    def __init__(self, fieldname, minchars, maxchars, discardspaces=False, analyzerclass=NgramAnalyzer):
        """
        :param fieldname: The field to search.
        :param minchars: The minimum gram size the text was indexed with.
        :param maxchars: The maximum gram size the text was indexed with.
        :param discardspaces: If False, grams containing spaces are made into
            optional clauses of the query. If True, grams containing spaces are
            ignored.
        :param analyzerclass: An analyzer class. The default is the standard
            NgramAnalyzer. The parser will instantiate this analyzer with the
            gram size set to the maximum usable size based on the input string.
        """
        self.fieldname = fieldname
        self.minchars = minchars
        self.maxchars = maxchars
        self.discardspaces = discardspaces
        self.analyzerclass = analyzerclass

    def parse(self, input):
        required = []
        optional = []
        gramsize = max(self.minchars, min(self.maxchars, len(input)))
        if gramsize > len(input):
            return NullQuery(input)
        discardspaces = self.discardspaces
        for t in self.analyzerclass(gramsize)(input):
            gram = t.text
            if ' ' in gram:
                if not discardspaces:
                    optional.append(gram)
            else:
                required.append(gram)

        if required:
            fieldname = self.fieldname
            andquery = And([ Term(fieldname, g) for g in required ])
            if optional:
                orquery = Or([ Term(fieldname, g) for g in optional ])
                return AndMaybe([andquery, orquery])
            return andquery
        else:
            return NullQuery