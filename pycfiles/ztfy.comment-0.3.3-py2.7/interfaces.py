# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/comment/interfaces.py
# Compiled at: 2012-06-26 16:37:02
__docformat__ = 'restructuredtext'
from zope.annotation.interfaces import IAttributeAnnotatable
from zope.security.interfaces import IPrincipal
from zope.interface import Interface
from zope.interface.common.sequence import IReadSequence, IWriteSequence
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from zope.schema import Datetime, Object, Choice, Set
from schema import CommentField
from ztfy.security.schema import Principal
from ztfy.comment import _

class ICommentable(IAttributeAnnotatable):
    """Marker interface for commentable contents"""
    pass


class IComment(ICommentable):
    """Base class for comments"""
    date = Datetime(title=_('Creation date'), description=_('Date and time of comment creation'), required=True, readonly=True)
    principal_id = Principal(title=_('Creation principal'), description=_('The ID of the principal who added this comment'), required=True, readonly=True)
    principal = Object(schema=IPrincipal, title=_('Comment creator'), description=_('Principal who added the comment'), required=True, readonly=True)
    body = CommentField(title=_('Comment body'), description=_('Main content of this comment'), required=True)
    body_renderer = Choice(title=_('Comment renderer'), description=_("Name of utility used to render comment's body"), required=True, vocabulary='SourceTypes', default='zope.source.plaintext')
    in_reply_to = Object(title=_("Comment's parent"), description=_('Previous comment to which this comment replies'), required=False, schema=ICommentable)
    tags = Set(title=_('Comment tags'), description=_('A list of internal tags used to classify comments'), required=False)

    def getAge():
        """Return comment age"""
        pass

    def render(request=None):
        """Render comment body"""
        pass


class ICommentsListReader(IReadSequence):
    """Base class reader for comments"""
    pass


class ICommentsListWriter(IWriteSequence):
    """Base class writer for comments"""
    pass


class ICommentsList(IReadSequence, IWriteSequence):
    """Main class for comments list"""
    pass


class ICommentsReader(Interface):
    """Main reader class for comments"""

    def getComments(tag=None):
        """Get comments list"""
        pass


class ICommentsWriter(Interface):
    """Main writer class for comments"""

    def addComment(body, in_reply_to=None, renderer=None, tags=None):
        """Add a new comment"""
        pass


class IComments(ICommentsReader, ICommentsWriter):
    """Main class for comments"""
    pass


class ICommentAddedEvent(IObjectModifiedEvent):
    """Marker interface for comment added events"""
    comment = Object(title=_('Added comment'), description=_('The comment object which was added'), required=True, schema=IComment)