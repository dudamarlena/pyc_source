# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/alchemy/vocabulary.py
# Compiled at: 2015-09-10 10:38:05
from zope.schema.interfaces import IVocabularyFactory
from ztfy.alchemy.interfaces import IAlchemyEngineUtility
from zope.componentvocabulary.vocabulary import UtilityVocabulary
from zope.interface import classProvides

class AlchemyEnginesVocabulary(UtilityVocabulary):
    """SQLAlchemy engines vocabulary"""
    classProvides(IVocabularyFactory)
    interface = IAlchemyEngineUtility
    nameOnly = True