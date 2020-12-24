# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/archetypes/languagebugfix/patch.py
# Compiled at: 2010-03-13 19:31:04
from zope.component import queryUtility
from logging import INFO, DEBUG
from Products.Archetypes import PloneMessageFactory as _
from Products.Archetypes.debug import log
from Products.Archetypes.utils import DisplayList, shasattr
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.ExtensibleMetadata import ExtensibleMetadata
try:
    from plone.i18n.locales.interfaces import IMetadataLanguageAvailability
    HAS_PLONE_I18N = True
except ImportError:
    HAS_PLONE_I18N = False

_enabled = []

def AlreadyApplied(patch):
    if patch in _enabled:
        return True
    _enabled.append(patch)
    return False


def languages(self):
    """Vocabulary method for the language field
    """
    lt = getToolByName(self, 'portal_languages')
    use_combined = lt.use_combined_language_codes
    util = None
    if HAS_PLONE_I18N:
        util = queryUtility(IMetadataLanguageAvailability)
    if util is None:
        languages = getattr(self, 'availableLanguages', None)
        if callable(languages):
            languages = languages()
        if languages is None:
            return DisplayList((('en', 'English'), ('fr', 'French'), ('es', 'Spanish'), ('pt', 'Portuguese'), ('ru', 'Russian')))
    else:
        languages = util.getLanguageListing(combined=use_combined)
        languages.sort(lambda x, y: cmp(x[1], y[1]))
        languages.insert(0, ('', _('Language neutral (site default)')))
    return DisplayList(languages)


def FixLanguageBug():
    if AlreadyApplied('FixLanguageBug'):
        return
    ExtensibleMetadata.languages_old = ExtensibleMetadata.languages
    ExtensibleMetadata.languages = languages
    log('Patched language field vocabulary', level=INFO)