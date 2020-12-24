# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Applications/Plone/Python-2.7/lib/python2.7/site-packages/medialog/dexterityview/vocabulary.py
# Compiled at: 2015-07-06 11:56:23
from Products.CMFCore.utils import getToolByName
from zope.interface import directlyProvides
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.schema.interfaces import IVocabularyFactory
from plone import api
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('medialog.dexterityview')

def format_size(size):
    return ('').join(size).split(' ')[0]


def ImageSizeVocabulary(context):
    portal_properties = api.portal.get_tool(name='portal_properties')
    if 'imaging_properties' in portal_properties.objectIds():
        sizes = portal_properties.imaging_properties.getProperty('allowed_sizes')
        sizes += ('original', )
        terms = [ SimpleTerm(value=format_size(pair), token=format_size(pair), title=pair) for pair in sizes ]
        return SimpleVocabulary(terms)
    else:
        return SimpleVocabulary([
         SimpleTerm('mini', 'mini', 'Mini'),
         SimpleTerm('preview', 'preview', 'Preview'),
         SimpleTerm('large', 'large', 'Large'),
         SimpleTerm('original', 'original', 'Original')])

    return SimpleVocabulary(terms)


directlyProvides(ImageSizeVocabulary, IVocabularyFactory)