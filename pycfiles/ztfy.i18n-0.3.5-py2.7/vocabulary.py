# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/i18n/vocabulary.py
# Compiled at: 2012-06-20 11:46:34
from z3c.language.negotiator.interfaces import INegotiatorManager
from z3c.language.switch.interfaces import IAvailableLanguagesVocabulary
from zope.schema.interfaces import IVocabularyFactory
from ztfy.i18n.interfaces import II18nManager, II18nManagerInfo
from zope.component import queryUtility
from zope.interface import implements, classProvides
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from ztfy.utils import getParent

class I18nLanguagesVocabulary(SimpleVocabulary):
    """A vocabulary of available languages in a given context
    
    Available languages are searched for in this order :
     - look for the first I18nManager parent
     - look for I18n negociator utility
     - fallback to 'en'
    """
    implements(IAvailableLanguagesVocabulary)
    classProvides(IVocabularyFactory)

    def __init__(self, context):
        langs = []
        terms = []
        parent = getParent(context, II18nManager, allow_context=False)
        if parent is not None:
            info = II18nManagerInfo(parent, None)
            if info is not None:
                langs = info.availableLanguages
        if not langs:
            negotiator = queryUtility(INegotiatorManager)
            if negotiator is not None:
                langs = negotiator.offeredLanguages
        for lang in langs:
            terms.append(SimpleTerm(lang))

        terms.sort()
        super(I18nLanguagesVocabulary, self).__init__(terms)
        return