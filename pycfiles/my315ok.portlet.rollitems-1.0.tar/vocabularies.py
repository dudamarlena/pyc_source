# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/zptest/webhosts/sites/src/my315ok.portlet.rollitems/my315ok/portlet/rollitems/vocabularies.py
# Compiled at: 2009-05-26 05:57:46
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from zope.app.schema.vocabulary import IVocabularyFactory
from zope.interface import implements
from my315ok.portlet.rollitems import RollPortletMessageFactory as _
from collective.portlet.pixviewer import PixviewerPortletMessageFactory as _a
roll_dire_unit = [('top', 'up direction', _('roll up')), ('down', 'down direction', _('roll down')), ('left', 'left direction', _('roll left')), ('right', 'right direction', _('roll right'))]
roll_dire_terms = [ SimpleTerm(value, token, title) for (value, token, title) in roll_dire_unit ]

class RollDirectionVocabulary(object):
    """ Ad Unit sizes """
    __module__ = __name__
    implements(IVocabularyFactory)

    def __call__(self, context):
        return SimpleVocabulary(roll_dire_terms)


RollDirectionVocabularyFactory = RollDirectionVocabulary()
image_size = [
 (
  'thumb', 'thumb image', _a('thumb image')), ('mini', 'mini image', _a('mini image')), ('preview', 'preview image', _a('preview image')), ('large', 'large image', _a('large image'))]
image_size_terms = [ SimpleTerm(value, token, title) for (value, token, title) in image_size ]

class ImageSizeVocabulary(object):
    """ Ad Unit sizes """
    __module__ = __name__
    implements(IVocabularyFactory)

    def __call__(self, context):
        return SimpleVocabulary(image_size_terms)


ImageSizeVocabularyFactory = ImageSizeVocabulary()