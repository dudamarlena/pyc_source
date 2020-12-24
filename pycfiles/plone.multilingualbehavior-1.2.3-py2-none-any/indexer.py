# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/plone/multilingual/indexer.py
# Compiled at: 2013-10-15 10:29:21
from plone.indexer import indexer
from plone.multilingual.interfaces import ITranslatable, ITG, ILanguage

@indexer(ITranslatable)
def itgIndexer(obj):
    return ITG(obj, None)


@indexer(ITranslatable)
def LanguageIndexer(object, **kw):
    language = ILanguage(object).get_language()
    return language