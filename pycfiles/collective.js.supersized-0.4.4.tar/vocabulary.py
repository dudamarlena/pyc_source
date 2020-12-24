# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/espenmoe-nilssen/Plone/zinstance/src/collective.js.supersized/collective/js/supersized/vocabulary.py
# Compiled at: 2014-09-17 10:19:31
from Products.CMFCore.utils import getToolByName
from zope.interface import directlyProvides
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.schema.interfaces import IVocabularyFactory
try:
    from zope.app.component.hooks import getSite
except ImportError:
    from zope.component.hooks import getSite

from zope.i18nmessageid import MessageFactory
_ = MessageFactory('collective.js.supersized')

def format_size(size):
    return ('').join(size).split(' ')[0]


def ImageSizeVocabulary(context):
    site = getSite()
    portal_properties = getToolByName(site, 'portal_properties', None)
    if 'imaging_properties' in portal_properties.objectIds():
        sizes = portal_properties.imaging_properties.getProperty('allowed_sizes')
        sizes += ('original', )
        terms = [ SimpleTerm(value=format_size(pair), token=format_size(pair), title=pair) for pair in sizes ]
        return SimpleVocabulary(terms)
    else:
        return SimpleVocabulary([
         SimpleTerm('preview', 'preview', 'Preview'),
         SimpleTerm('large', 'large', 'Large')])
        return SimpleVocabulary(terms)


directlyProvides(ImageSizeVocabulary, IVocabularyFactory)

def TransitionVocabulary(context):
    return SimpleVocabulary([
     SimpleTerm(0, 0, _('label_transition0', default='None')),
     SimpleTerm(1, 1, _('label_transition1', default='Fade')),
     SimpleTerm(2, 2, _('label_transition2', default='Slide Top')),
     SimpleTerm(3, 3, _('label_transition3', default='Slide Right')),
     SimpleTerm(4, 4, _('label_transition4', default='Slide Bottom')),
     SimpleTerm(5, 5, _('label_transition5', default='Slide Left')),
     SimpleTerm(6, 6, _('label_transition6', default='Carousel Right')),
     SimpleTerm(7, 7, _('label_transition7', default='Carousel Left'))])


directlyProvides(TransitionVocabulary, IVocabularyFactory)