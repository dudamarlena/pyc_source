# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/blog/vocabulary.py
# Compiled at: 2012-06-26 16:33:07
__docformat__ = 'restructuredtext'
from zope.publisher.interfaces.browser import IBrowserSkinType
from zope.schema.interfaces import IVocabularyFactory
from ztfy.blog.layer import IZTFYBlogFrontLayer
from zope.component import getUtilitiesFor
from zope.componentvocabulary.vocabulary import UtilityVocabulary, UtilityTerm
from zope.interface import classProvides
from zope.i18n import translate
from zope.schema import getFields
from ztfy.utils.request import getRequest

class SkinsVocabulary(UtilityVocabulary):
    classProvides(IVocabularyFactory)
    interface = IBrowserSkinType
    nameOnly = True

    def __init__(self, context, **kw):
        request = getRequest()
        utils = [ (name, translate(getFields(util)['label'].title, context=request)) for name, util in getUtilitiesFor(self.interface, context) if util.extends(IZTFYBlogFrontLayer)
                ]
        self._terms = dict((title, UtilityTerm(name, title)) for name, title in utils)


def getValues(parent, context, output):
    output.append((parent, context))
    for item in context.values():
        getValues(context, item, output)