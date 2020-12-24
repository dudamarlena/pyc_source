# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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