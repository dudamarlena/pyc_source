# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gyst/plonesocial.buildout/src/plonesocial.microblog/plonesocial/microblog/interfaces.py
# Compiled at: 2014-03-11 12:09:55
from zope import schema
from zope.interface import Attribute
from zope.interface import Interface
from plone.uuid.interfaces import IUUIDAware
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('plonesocial.microblog')

class IStatusUpdate(Interface):
    """A single 'tweet'."""
    id = schema.Int(title=_('A longint unique status id'))
    text = schema.Text(title=_('add_statusupdate_button', default='What are you doing?'))
    creator = schema.TextLine(title=_('Author name (for display)'))
    userid = schema.TextLine(title=_('Userid'))
    creation_date = schema.Date(title=_('Creation date'))
    tags = Attribute('Tags/keywords')
    context_UUID = Attribute('UUID of IMicroblogContext (e.g. a workspace)')
    context_object = Attribute('UUID of context object (e.g. a Page)')


class IStatusContainer(Interface):
    """Manages read/write access to, and storage of,
    IStatusUpdate instances.

    IStatusContainer provides a subset of a ZODB IBTree interface.

    Some IBTree methods are blocked because they would destroy
    consistency of the internal data structures.

    IStatusContainer manages a more complex data structure than
    just a BTree: it also provides for user and tag indexes.
    These are covered in additional methods.
    """

    def add(status):
        """Add a IStatusUpdate.

        Actual storage may be queued for later insertion by
        the implementation.

        Returns 1 on completion of synchronous insertion.
        Returns 0 when the actual insertion is queued for later processing.
        """
        pass

    def clear():
        """Empty the status storage and all indexes."""
        pass

    def get(key):
        """Fetch an IStatusUpdate by IStatusUpdate.id key."""
        pass

    def items(min=None, max=None, limit=100, tag=None):
        """BTree compatible accessor.
        min and max are longint IStatusUpdate.id keys.
        limit returns [:limit] most recent items
        tag 'foo' filters status text on hashtag '#foo'
        """
        pass

    def keys(min=None, max=None, limit=100, tag=None):
        """BTree compatible accessor.
        min and max are longint IStatusUpdate.id keys.
        limit returns [:limit] most recent items
        tag 'foo' filters status text on hashtag '#foo'
        """
        pass

    def values(min=None, max=None, limit=100, tag=None):
        """BTree compatible accessor.
        min and max are longint IStatusUpdate.id keys.
        limit returns [:limit] most recent items
        tag 'foo' filters status text on hashtag '#foo'
        """
        pass

    iteritems = items
    iterkeys = keys
    itervalues = values

    def user_items(users, min=None, max=None, limit=100, tag=None):
        """Filter (key, IStatusUpdate) items by iterable of userids.
        min and max are longint IStatusUpdate.id keys.
        limit returns [:limit] most recent items
        tag 'foo' filters status text on hashtag '#foo'
        """
        pass

    def user_keys(users, min=None, max=None, limit=100, tag=None):
        """Filter IStatusUpdate keys by iterable of userids.
        min and max are longint IStatusUpdate.id keys.
        limit returns [:limit] most recent items
        tag 'foo' filters status text on hashtag '#foo'
        """
        pass

    def user_values(users, min=None, max=None, limit=100, tag=None):
        """Filter IStatusUpdate values by iterable of userids.
        min and max are longint IStatusUpdate.id keys.
        limit returns [:limit] most recent items
        tag 'foo' filters status text on hashtag '#foo'
        """
        pass

    def context_items(context, min=None, max=None, limit=100, tag=None):
        """Filter (key, IStatusUpdate) items by IMicroblogContext object.
        min and max are longint IStatusUpdate.id keys.
        limit returns [:limit] most recent items
        context <object> filters on StatusUpdates keyed to that context's UUID.
        """
        pass

    def context_keys(context, min=None, max=None, limit=100, tag=None):
        """Filter IStatusUpdate keys by IMicroblogContext object.
        min and max are longint IStatusUpdate.id keys.
        limit returns [:limit] most recent items
        tag 'foo' filters status text on hashtag '#foo'
        """
        pass

    def context_values(context, min=None, max=None, limit=100, tag=None):
        """Filter IStatusUpdate values by IMicroblogContext object.
        min and max are longint IStatusUpdate.id keys.
        limit returns [:limit] most recent items
        tag 'foo' filters status text on hashtag '#foo'

        """
        pass


class IMicroblogTool(IStatusContainer):
    """Provide IStatusContainer as a site utility."""
    pass


class IMicroblogContext(IUUIDAware):
    """Marker interface for non-SiteRoot objects with a local microblog.
    Such objects should be adaptable to provide a UUID.
    """
    pass