# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Applications/Plone/zinstance/src/collective.ptg.tile/collective/ptg/tile/vocabularies.py
# Compiled at: 2014-02-04 07:34:11
from Products.CMFCore.utils import getToolByName
from zope.interface import directlyProvides
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.schema.interfaces import IVocabularyFactory
from plone import api
from collective.plonetruegallery.interfaces import IGallery

def GalleryVocabulary(context):
    portal = api.portal.get()
    catalog = portal.portal_catalog
    results = catalog(object_provides=IGallery.__identifier__)
    galleries = []
    for result in results:
        if str(result.getObject().getLayout()) == 'galleryview':
            galleries.append(result.getPath())

    terms = [ SimpleTerm(value=pair, token=pair, title=pair) for pair in galleries ]
    return SimpleVocabulary(terms)


directlyProvides(GalleryVocabulary, IVocabularyFactory)