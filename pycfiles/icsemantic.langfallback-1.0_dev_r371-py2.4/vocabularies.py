# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/icsemantic/langfallback/vocabularies.py
# Compiled at: 2008-10-06 10:31:06
"""
"""
from zope.schema import vocabulary
from zope.app.schema.vocabulary import IVocabularyFactory
from zope.interface import implements
from zope.component import getUtility
from zope.component import queryUtility
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import ITypesTool
from Products.CMFCore.interfaces import IPropertiesTool
from Products.CMFPlone.utils import safe_unicode
from icsemantic.core.i18n import _
from icsemantic.core.config import HAS_PLONE3
import cgi
if HAS_PLONE3:
    from plone.i18n.locales.interfaces import IContentLanguageAvailability
else:
    from Products.PloneLanguageTool import availablelanguages

class AvailableLanguagesVocabulary(object):
    """

        TODO: Remove in next versions.

    Test ContentTypes vocab,

    """
    __module__ = __name__
    implements(IVocabularyFactory)

    def __call__(self, context):
        context = getattr(context, 'context', context)
        portal_languages = getToolByName(context, 'portal_languages')
        terms = portal_languages.listSupportedLanguages()
        return vocabulary.SimpleVocabulary([ vocabulary.SimpleTerm(term[0], title=safe_unicode(term[1])) for term in terms ])


AvailableLanguagesVocabularyFactory = AvailableLanguagesVocabulary()