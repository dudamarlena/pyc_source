# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/cache/vocabulary.py
# Compiled at: 2012-06-11 15:33:55
from zope.schema.interfaces import IVocabularyFactory
from ztfy.cache.metadirectives import ICacheProxyHandlerBase
from zope.componentvocabulary.vocabulary import UtilityVocabulary
from zope.interface import classProvides

class CacheProxyHandlerVocabulary(UtilityVocabulary):
    """Cache proxy vocabulary"""
    classProvides(IVocabularyFactory)
    interface = ICacheProxyHandlerBase
    nameOnly = True