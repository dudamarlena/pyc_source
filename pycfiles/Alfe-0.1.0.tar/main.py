# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/alfanous/main.py
# Compiled at: 2015-06-30 06:52:38
__doc__ = '\nThe main module that relay all the modules.\n\n'
from alfanous.Searching import QSearcher, QReader
from alfanous.Indexing import QseDocIndex, ExtDocIndex, BasicDocIndex
from alfanous.ResultsProcessing import Qhighlight, QPaginate
from alfanous.QueryProcessing import QuranicParser, StandardParser, FuzzyQuranicParser
from alfanous.Suggestions import QAyaSpellChecker, QSubjectSpellChecker, concat_suggestions, QWordChecker

class BasicSearchEngine:
    """
    the basic search engine

    """

    def __init__(self, qdocindex, qparser, mainfield, otherfields, qsearcher, qreader, qspellcheckers, qhighlight):
        self.OK = False
        if qdocindex.OK:
            self._docindex = qdocindex
            self._schema = self._docindex.get_schema()
            self._parser = qparser(self._schema, mainfield=mainfield, otherfields=otherfields)
            self._searcher = qsearcher(self._docindex, self._parser)
            self._reader = qreader(self._docindex)
            self._spellcheckers = map(lambda X: X(self._docindex, self._parser), qspellcheckers)
            self._highlight = qhighlight
            self.OK = True

    def search_all(self, querystr, limit=6236, sortedby='score', reverse=False):
        u"""
        search in the quran

                >>> results,terms=search_all(u"الحمد",limit=10,sortby="mushaf")
                >>> print ",".join([term[1] for term in list(terms)])
                الحمد
                >>> for r in results:
                >>>         print "(" + r["aya_id"] + "," + r["sura_id"] + ") :" + u"<p>" + Qhighlight(r["aya_"], terms) + u"</p>"
                (2,1) :<p><span style="color:red;font-size:100.0%"><b>الْحَمْدُ</b></span> لِلَّهِ رَبِّ الْعَالَمِينَ</p>

        @param querystr: the query
        @type querystr: unicode
        @param limit: the limit of results
        @type limit: int
        @param sortedby: the methode of sorting the results
        @type sortedby: string
        @return: the lists of terms and results

        """
        if querystr.__class__ is not unicode:
            querystr = querystr.decode('utf-8')
        results, terms, searcher = self._searcher.search(querystr, limit, sortedby, reverse)
        return (
         results, list(self._reader.term_stats(terms)), searcher)

    def most_frequent_words(self, nb, fieldname):
        return list(self._reader.reader.most_frequent_terms(fieldname, nb))

    def suggest_all(self, querystr):
        u"""suggest the missed words

            >>> for key, value in suggest_all(u" عاصمو ").items():
            >>>    print key, ":", ",".join(value)
            عاصمو : عاصم
        """
        if querystr.__class__ is not unicode:
            querystr = querystr.decode('utf-8')
        return concat_suggestions(map(lambda X: X.QSuggest(querystr), self._spellcheckers))

    def highlight(self, text, terms, type='css', strip_vocalization=True):
        return self._highlight(text, terms, type, strip_vocalization)

    def find_extended(self, query, defaultfield):
        """
        a simple search operation on extended document index

        """
        searcher = self._docindex.get_searcher()()
        return (
         searcher.find(defaultfield, query), searcher)

    def list_values(self, fieldname, double=False, conditions=[]):
        """ list all stored values of a field  """
        return self._reader.list_values(fieldname, double=double, conditions=conditions)

    def __call__(self):
        return self.OK


def QuranicSearchEngine(indexpath='../../indexes/main/', qparser=QuranicParser):
    return BasicSearchEngine(qdocindex=QseDocIndex(indexpath), qparser=qparser, mainfield='aya', otherfields=[], qsearcher=QSearcher, qreader=QReader, qspellcheckers=[
     QAyaSpellChecker, QSubjectSpellChecker], qhighlight=Qhighlight)


def FuzzyQuranicSearchEngine(indexpath='../indexes/main/', qparser=FuzzyQuranicParser):
    return BasicSearchEngine(qdocindex=QseDocIndex(indexpath), qparser=qparser, mainfield='aya', otherfields=[
     'subject'], qsearcher=QSearcher, qreader=QReader, qspellcheckers=[
     QAyaSpellChecker, QSubjectSpellChecker], qhighlight=Qhighlight)


def TraductionSearchEngine(indexpath='../indexes/extend/', qparser=StandardParser):
    """             """
    return BasicSearchEngine(qdocindex=ExtDocIndex(indexpath), qparser=qparser, mainfield='text', otherfields=[], qsearcher=QSearcher, qreader=QReader, qspellcheckers=[], qhighlight=Qhighlight)


def WordSearchEngine(indexpath='../indexes/word/', qparser=StandardParser):
    return BasicSearchEngine(qdocindex=BasicDocIndex(indexpath), qparser=qparser, mainfield='normalized', otherfields=[
     'word', 'spelled'], qsearcher=QSearcher, qreader=QReader, qspellcheckers=[
     QWordChecker], qhighlight=Qhighlight)