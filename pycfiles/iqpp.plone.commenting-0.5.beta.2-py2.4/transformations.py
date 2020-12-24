# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.10.1-i386/egg/iqpp/plone/commenting/adapters/transformations.py
# Compiled at: 2007-10-06 06:19:54
from zope.interface import implements
from zope.component import adapts
from Products.CMFPlone.utils import safe_unicode
from iqpp.plone.commenting.interfaces import IComment
from iqpp.plone.commenting.interfaces import ICommentTransformations

class CommentTransformations(object):
    """An adapter for IComments, which provides text transformation from 
    intelligenttext to HTML.
    """
    __module__ = __name__
    implements(ICommentTransformations)
    adapts(IComment)

    def __init__(self, context):
        """
        """
        self.context = context

    def transformMessage(self):
        """
        """
        try:
            from plone.intelligenttext.transforms import convertWebIntelligentPlainTextToHtml as convert
        except ImportError:
            transformed_message = self.context.message.replace('\n', '<br/>')
        else:
            transformed_message = convert(self.context.message)

        self.context.transformed_message = safe_unicode(transformed_message)