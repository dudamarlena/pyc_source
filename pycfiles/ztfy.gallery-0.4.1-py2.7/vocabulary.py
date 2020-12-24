# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/gallery/vocabulary.py
# Compiled at: 2013-03-14 19:01:43
__docformat__ = 'restructuredtext'
from copy import copy
from zope.publisher.interfaces.browser import IBrowserSkinType
from zope.schema.interfaces import IVocabularyFactory
from ztfy.gallery.interfaces import IGalleryParagraphRenderer
from ztfy.skin.interfaces import ISkinnable
from zope.component import getAdapters, queryUtility
from zope.i18n import translate
from zope.interface import classProvides
from zope.publisher.browser import applySkin
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from ztfy.utils.request import getRequest
from ztfy.utils.traversing import getParent

class GalleryParagraphRenderersVocabulary(SimpleVocabulary):
    classProvides(IVocabularyFactory)
    interface = IGalleryParagraphRenderer

    def __init__(self, context):
        request = getRequest()
        fake = copy(request)
        parent = getParent(context, ISkinnable)
        if parent is not None:
            skin = queryUtility(IBrowserSkinType, parent.getSkin())
            if skin is not None:
                applySkin(fake, skin)
            adapters = ((name, translate(adapter.label, context=request)) for name, adapter in getAdapters((context, fake), self.interface))
            terms = [ SimpleTerm(name, name, title) for name, title in adapters ]
        else:
            terms = []
        super(GalleryParagraphRenderersVocabulary, self).__init__(terms)
        return