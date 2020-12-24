# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/thet-data/data/dev/htu/bda.htu.buildout/src/collective.teaser/collective/teaser/vocabularies.py
# Compiled at: 2013-03-13 08:34:51
from zope.interface import directlyProvides
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from zope.i18nmessageid import MessageFactory
from plone.app.imaging.utils import getAllowedSizes
_ = MessageFactory('collective.teaser')

def ImportanceVocabulary(context):
    items = [
     (
      _('importance_highest', default='Highest importance'), '4'),
     (
      _('importance_high', default='High importance'), '3'),
     (
      _('importance_normal', default='Normal importance'), '2'),
     (
      _('importance_low', default='Low importance'), '1')]
    return SimpleVocabulary.fromItems(items)


directlyProvides(ImportanceVocabulary, IVocabularyFactory)

def ImageScaleVocabulary(context):
    allowed_sizes = getAllowedSizes()
    items = [ ('%s(%s, %s)' % (key, value[0], value[1]), key) for key, value in allowed_sizes.items() if allowed_sizes
            ]
    return SimpleVocabulary.fromItems(items)


directlyProvides(ImageScaleVocabulary, IVocabularyFactory)