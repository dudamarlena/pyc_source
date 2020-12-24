# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.10.1-i386/egg/iqpp/plone/commenting/content.py
# Compiled at: 2007-10-06 06:19:54
from datetime import datetime
from persistent import Persistent
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from Products.CMFPlone.utils import safe_unicode
from iqpp.plone.commenting.config import REVIEW_STATES
from iqpp.plone.commenting.interfaces import IComment
from iqpp.plone.commenting.interfaces import ICommentAddedEvent

class Comment(Persistent):
    """A comment. 
    """
    __module__ = __name__
    implements(IComment)
    id = FieldProperty(IComment['id'])
    reply_to = FieldProperty(IComment['reply_to'])
    member_id = FieldProperty(IComment['member_id'])
    name = FieldProperty(IComment['name'])
    email = FieldProperty(IComment['email'])
    subject = FieldProperty(IComment['subject'])
    message = FieldProperty(IComment['message'])
    transformed_message = FieldProperty(IComment['transformed_message'])
    review_state = FieldProperty(IComment['review_state'])
    created = FieldProperty(IComment['created'])
    modified = FieldProperty(IComment['modified'])

    def __init__(self, id, reply_to, subject, message, member_id='', name='', email='', review_state='pending'):
        """
        """
        self.id = safe_unicode(id)
        self.reply_to = safe_unicode(reply_to)
        self.member_id = safe_unicode(member_id)
        self.name = safe_unicode(name)
        self.email = safe_unicode(email)
        self.subject = safe_unicode(subject)
        self.message = safe_unicode(message)
        self.transformed_message = ''
        self.review_state = review_state
        self.created = datetime.now()
        self.modified = datetime.now()

    def UID(self):
        """
        """
        return self.id

    def publish(self):
        self.review_state = 'published'
        assert self.review_state in REVIEW_STATES

    def reject(self):
        self.review_state = 'private'
        assert self.review_state in REVIEW_STATES

    def submit(self):
        self.review_state = 'pending'
        assert self.review_state in REVIEW_STATES


class CommentAddedEvent(object):
    """An event which is sent when a comment has been added.
    """
    __module__ = __name__
    implements(ICommentAddedEvent)

    def __init__(self, context, comment):
        """
        """
        self.context = context
        self.comment = comment