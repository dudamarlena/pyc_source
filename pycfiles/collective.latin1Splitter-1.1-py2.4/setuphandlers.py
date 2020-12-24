# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/collective/latin1Splitter/setuphandlers.py
# Compiled at: 2009-12-22 10:28:10
from Products.CMFCore.utils import getToolByName
from Products.ZCTextIndex.ZCTextIndex import manage_addLexicon

class largs:
    __module__ = __name__

    def __init__(self, **kw):
        self.__dict__.update(kw)


def createZCTextIndexLatin1Lexicon(catalog, lid):
    manage_addLexicon(catalog, lid, elements=[largs(group='Case Normalizer', name='Unicode Case Normalizer'), largs(group='Stop Words', name=" Don't remove stop words"), largs(group='Word Splitter', name='Unicode Whitespace splitter'), largs(group='Latin1 Word Splitter', name='Latin1 splitter')])


class Generator:
    __module__ = __name__

    def __init__(self, site):
        self.site = site

    def updatePloneLexicon(self):
        catalog = getToolByName(self.site, 'portal_catalog')
        catalog._delObject('plone_lexicon')
        createZCTextIndexLatin1Lexicon(catalog, 'plone_lexicon')


def importVarious(context):
    if context.readDataFile('collective.latin1Splitter_importVarious.txt') is None:
        return
    gen = Generator(context.getSite())
    gen.updatePloneLexicon()
    return