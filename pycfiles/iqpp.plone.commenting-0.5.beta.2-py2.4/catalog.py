# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.10.1-i386/egg/iqpp/plone/commenting/catalog.py
# Compiled at: 2007-10-06 06:19:54
from zope.component.interfaces import ComponentLookupError
from Products.CMFPlone.CatalogTool import registerIndexableAttribute
from iqpp.plone.commenting.interfaces import ICommenting
from iqpp.plone.commenting.interfaces import ICommentable

def published_comments(object, portal, **kwargs):
    try:
        comments = []
        for comment in ICommenting(object).getAllComments():
            if comment.review_state == 'published':
                comments.append(comment.id)

        return comments
    except (ComponentLookupError, TypeError, ValueError):
        raise AttributeError


def pending_comments(object, portal, **kwargs):
    try:
        comments = []
        for comment in ICommenting(object).getAllComments():
            if comment.review_state == 'pending':
                comments.append(comment.id)

        return comments
    except (ComponentLookupError, TypeError, ValueError):
        raise AttributeError


registerIndexableAttribute('published_comments', published_comments)
registerIndexableAttribute('pending_comments', pending_comments)