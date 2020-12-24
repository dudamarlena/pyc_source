# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /opt/Plone-4.3.7-was-4.2.1/zeocluster/src/Products.ATSuccessStory/Products/ATSuccessStory/vocabularies.py
# Compiled at: 2015-12-17 03:21:31
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary
from Products.CMFCore.utils import getToolByName
from zope.interface import implements, implementer, alsoProvides
from zope.schema.interfaces import IVocabulary, IVocabularyFactory
from Products.ATSuccessStory import _

@implementer(IVocabulary)
def existingSSFolders(context):
    pc = getToolByName(context, 'portal_catalog')
    pu = getToolByName(context, 'portal_url')
    portal = pu.getPortalObject()
    portal_path = ('/').join(portal.getPhysicalPath())
    results = pc.searchResults(portal_type='ATSuccessStoryFolder')
    terms = [
     SimpleVocabulary.createTerm(portal_path, portal_path, _('Global'))]
    for value in results:
        path = value.getPath()
        terms.append(SimpleVocabulary.createTerm(path, path, '%s - %s' % (value.Title, value.getPath())))

    return SimpleVocabulary(terms)


alsoProvides(existingSSFolders, IVocabularyFactory)