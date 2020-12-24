# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/icsemantic/thesaurus/patches.py
# Compiled at: 2008-10-06 10:31:07
"""Monkey patches
"""
from Products.LinguaPlone.I18NBaseObject import I18NBaseObject
from icsemantic.thesaurus.Thesaurus import thesaurus_utility

def get_translations(portal, k, lang=None):
    """Query the local thesaurus for translated concepts"""
    try:
        r = thesaurus_utility().get_equivalent(k, lang, exclude=False)
    except IndexError:
        r = []

    return r


def addTranslation(self, language, *args, **kwargs):
    """Do what Products.LinguaPlone.I18NBaseObject.addTranslation does
    but also add translations of the keywords to the translated
    version.
    """
    self.old_addTranslation(language, *args, **kwargs)
    canonical = self.getCanonical()
    translation = self.getTranslation(language)
    subject = canonical.Subject()
    translated_subject = []
    portal = self.portal_url.getPortalObject()
    for s in subject:
        translated_subject += get_translations(portal, s + '@' + self.getCanonicalLanguage(), lang=[language])

    translated_subject = map(lambda x: x[:-(len(language) + 1)], translated_subject)
    translation.setSubject(translated_subject)
    translation.reindexObject()


I18NBaseObject.old_addTranslation = I18NBaseObject.addTranslation
I18NBaseObject.addTranslation = addTranslation