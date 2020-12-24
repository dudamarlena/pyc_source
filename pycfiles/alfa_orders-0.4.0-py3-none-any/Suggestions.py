# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/alfanous/Suggestions.py
# Compiled at: 2015-06-30 06:52:38
__doc__ = '\nit contains  suggestions systems\n\n@author: Assem Chelli\n@contact: assem.ch [at] gmail.com\n@license: AGPL\n\n\n'
from alfanous.Support.whoosh.spelling import SpellChecker

class QSuggester(SpellChecker):
    """ the basic system of suggestions """

    def __init__(self, docindex, qparser, fields, spellindexname):
        storage = docindex.get_index().storage
        self._qparser = qparser
        self._reader = docindex.get_reader()
        self.fields = fields
        super(QSuggester, self).__init__(storage, indexname=spellindexname)

    def _filter_doubles(self, words):
        return list(set(words))

    def QSuggest(self, querystr):
        suggestion_result = {}
        missing = set()
        query = self._qparser.parse(querystr)
        query.existing_terms(self._reader, missing, reverse=True, phrases=True)
        for fieldname, termtext in missing:
            if fieldname in self.fields:
                suggestions = self._filter_doubles(self.suggest(termtext))
            else:
                suggestions = None
            if suggestions:
                suggestion_result[termtext] = suggestions

        return suggestion_result


def QAyaSpellChecker(docindex, qparser):
    """spellchecking the words of aya fields"""
    return QSuggester(docindex, qparser, fields=[
     'aya', 'uth', 'aya_', 'uth_'], spellindexname='AYA_SPELL')


def QSubjectSpellChecker(docindex, qparser):
    """spellchecking the words of aya fields"""
    return QSuggester(docindex, qparser, fields=[
     'subject', 'chapter', 'topic', 'subtopic'], spellindexname='Sub_SPELL')


def QWordChecker(docindex, qparser):
    """spellchecking the words"""
    return QSuggester(docindex, qparser, fields=[
     'word'], spellindexname='WORD_SPELL')


def concat_suggestions(listofsuggestions):
    """     """
    D = {}
    for unit in listofsuggestions:
        for key, values in unit.items():
            if D.has_key(key):
                D[key].extend[list(values)]
            else:
                D[key] = list(values)

    return D