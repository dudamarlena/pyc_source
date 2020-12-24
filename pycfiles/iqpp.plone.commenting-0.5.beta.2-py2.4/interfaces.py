# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.10.1-i386/egg/iqpp/plone/commenting/interfaces.py
# Compiled at: 2007-10-07 08:02:10
from zope import schema
from zope.i18nmessageid import MessageFactory
from zope.annotation.interfaces import IAttributeAnnotatable
from zope.interface import Interface
from zope.interface import Attribute
from zope.viewlet.interfaces import IViewletManager
from config import *
_ = MessageFactory('iqpp.plone.commenting')

class ICommentable(IAttributeAnnotatable):
    """A marker interface to mark an object as commentable.
    """
    __module__ = __name__


class IComment(Interface):
    """Represents a comment.
    """
    __module__ = __name__
    id = schema.TextLine(title=_('id'), description=_('The id of comment. Must be unique'), required=True)
    reply_to = schema.TextLine(title=_('reply_to'), description=_('The id of the item that this comment relates to'), default='', required=False)
    member_id = schema.TextLine(title=_('member_id'), description=_('The id of the member that created this comment (if not anonymous)'), default=None, required=False)
    name = schema.TextLine(title=_('Name'), description=_('Your Fullname'), default='', required=False)
    email = schema.TextLine(title=_('E-Mail'), description=_('Your E-Mail'), default='', required=False)
    subject = schema.TextLine(title=_('Subject'), description=_('The subject of the comment'), default='', required=True)
    message = schema.Text(title=_('Message'), description=_('The message of the comment.'), default='', required=True)
    transformed_message = schema.Text(title=_('Transformed Message'), description=_('The message of the comment, transformed to be safe.'), required=False)
    review_state = schema.Choice(title=_('Review state'), description=_('The state of the comment (pending, published, rejected)'), values=REVIEW_STATES, default='private', required=True)
    created = schema.Datetime(title=_('Date created'), required=True)
    modified = schema.Datetime(title=_('Date modified'), required=True)

    def submit(self):
        """submit the comment -> new review_state is 'pending'"""
        pass

    def reject(self):
        """reject the comment -> new review_state is 'private'"""
        pass

    def publish(self):
        """reject the comment -> new review_state is 'published'"""
        pass


class ICommentTransformations(Interface):
    """
    """
    __module__ = __name__

    def transformMessage():
        """Transforms a comment's message to arbitrary format. For instance
        to save html.
        """
        pass


class IGlobalCommenting(Interface):
    """Provides Methods for global commenting management.
    """
    __module__ = __name__

    def getPendingComments():
        """Returns all pending comments of a site.
        """
        pass

    def getCommentsForMember(member_id):
        """Returns all comments for member with given member_id.
        """
        pass


class ICommenting(Interface):
    """A interface which provides methods to manage comments for arbitrary 
    objects.
    """
    __module__ = __name__

    def addComment(reply_to, subject, message, member_id=None, name=None, email=None):
        """Adds a comment.
        """
        pass

    def deleteComment(id):
        """Deletes a comment by given unique id and its replies.
        """
        pass

    def deleteComments():
        """Deletes all comments of an object.
        """
        pass

    def editComment(id, subject, message):
        """Edits just the subject and the message of an comment. Used from
        members, which edit their own comments.
        """
        pass

    def getAllComments(id=None):
        """Returns all comments from object with given id. If id is None,
        returns all comments of the root object.
        """
        pass

    def getComment(id):
        """Returns a comment by given uniqe id.
        """
        pass

    def getComments(id=None):
        """Returns direct comments of object with given id. If id is None, 
        returns comments of root object.
        """
        pass

    def manageComment(id, reply_to, subject, message, member_id, name, email):
        """Manages all data of an a existing comment. Used from managers which 
        are allowed to change every piece of an comment.
        """
        pass


class ICommentingOptions(Interface):
    """
    """
    __module__ = __name__

    def getGlobalOption(name):
        """Decides from where the global option is taken. By default this is
        the value taken from the control panel.
        
        3rd-Party developer may overwrite this method to take it from 
        somewhere else, e.g. a product specific tool.
        """
        pass

    def getEffectiveOption(name):
        """Returns the effective option with given name, which means: return
        the local one if there is one, otherwise the global.
        """
        pass

    is_enabled = schema.Choice(title=_('Is enabled'), description=_('Are comments for this object enabled?'), vocabulary=schema.vocabulary.SimpleVocabulary.fromItems(DEFAULT_CHOICES), default='default')
    is_moderated = schema.Choice(title=_('Is moderated'), description=_('Are comments for this item moderated?'), vocabulary=schema.vocabulary.SimpleVocabulary.fromItems(DEFAULT_CHOICES), default='default')
    show_preview = schema.Choice(title=_('Show preview'), description=_('Must comments for this item be previewed prior to adding?'), vocabulary=schema.vocabulary.SimpleVocabulary.fromItems(DEFAULT_CHOICES), default='default')
    edit_own_comments = schema.List(title=_('Owner can edit comments'), description=_('User is allowed to edit own comment for this item, when it is in one of selected states.'), required=False, default=['default'], value_type=schema.Choice(__name__='edit_own_comments', title='Review State', vocabulary=schema.vocabulary.SimpleVocabulary.fromItems(REVIEW_STATES_CHOICES)))
    send_comment_added_mail = schema.Choice(title=_('Send email notifications'), description=_('Should an email be sent for every new comment on this item?'), vocabulary=schema.vocabulary.SimpleVocabulary.fromItems(DEFAULT_CHOICES), default='default')
    mail_to = schema.TextLine(title=_('Email recipient address'), description=_('The address to which notifications about new comments should be sent. Leave it blank to take the default recipient address.'), default=_(''), required=False)
    mail_from = schema.TextLine(title=_('Email sender address'), description=_('The email address that will be used as sender for mails notifying about a new comment. Leave it blank to take the default sender address.'), default=_(''), required=False)


class ICommentAddedEvent(Interface):
    """An event for: Comment has been added.
    """
    __module__ = __name__
    context = Attribute('The object which has been commented.')
    comment = Attribute('The new comment')


class ICommentingViewletManager(IViewletManager):
    """
    """
    __module__ = __name__