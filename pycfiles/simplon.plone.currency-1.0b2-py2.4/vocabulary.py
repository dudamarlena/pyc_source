# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/simplon/plone/currency/vocabulary.py
# Compiled at: 2007-09-08 18:44:19
from zope.app.schema.vocabulary import IVocabularyFactory
from zope.interface import implements
from zope.component import getUtility
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from simplon.plone.currency.interfaces import ICurrencyManager
from Products.CMFPlone import PloneMessageFactory as _
from simplon.plone.currency.currencies import currencies

class CurrencyVocabulary(object):
    """Vocabulary factory for currencies."""
    __module__ = __name__
    implements(IVocabularyFactory)

    def __call__(self, context):

        def morph(code, data):
            return (
             code, SimpleTerm(value=code, token=code, title=_('${code} ${description}', mapping=dict(code=code, description=data[0]))))

        items = [ morph(*cur) for cur in currencies.items() ]
        items.sort()
        return SimpleVocabulary([ item[1] for item in items ])


CurrencyVocabularyFactory = CurrencyVocabulary()

class SiteCurrencyVocabulary(object):
    """Vocabulary factory for currencies enabled in the site."""
    __module__ = __name__
    implements(IVocabularyFactory)

    def __call__(self, context):

        def morph(code):
            return (
             code, SimpleTerm(value=code, token=code, title=_('${code} ${description}', mapping=dict(code=code, description=currencies[code][0]))))

        manager = getUtility(ICurrencyManager)
        items = [ morph(cur) for cur in manager.currencies.keys() ]
        items.sort()
        return SimpleVocabulary([ item[1] for item in items ])


SiteCurrencyVocabularyFactory = SiteCurrencyVocabulary()