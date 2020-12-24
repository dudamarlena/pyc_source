# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wwp/twitter/portlets/wwp_twitter_portlet.py
# Compiled at: 2009-08-20 05:36:04
from zope.interface import Interface
from zope.interface import implements
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from zope import schema
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from wwp.twitter.portlets import wwp_twitter_portletMessageFactory as _
from plone.memoize.instance import memoize
import twitter

class Iwwp_twitter_portlet(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """
    __module__ = __name__
    Title = schema.TextLine(title=_('Portlet Title'), description=_('Enter the title of the portlet'), required=True)
    Feed_name = schema.TextLine(title=_('Twitter Username'), description=_('Enter the username of the twitter feed to display'), required=True)
    No_tweets = schema.TextLine(title=_('Number of tweets to display'), description=_('Enter the number of tweets to display'), required=True)


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """
    __module__ = __name__
    implements(Iwwp_twitter_portlet)

    def __init__(self, Title='', Feed_name='', No_tweets=5):
        self.Title = Title
        self.Feed_name = Feed_name
        self.No_tweets = No_tweets

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return 'WWP Twitter Portlet'


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """
    __module__ = __name__
    render = ViewPageTemplateFile('wwp_twitter_portlet.pt')

    @memoize
    def title(self):
        return self.data.Title

    @memoize
    def username(self):
        return self.data.Feed_name

    @memoize
    def get_tweets(self):
        username = self.data.Feed_name
        limit = int(self.data.No_tweets)
        twapi = twitter.Api()
        return twapi.GetUserTimeline(username)[:limit]


class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    __module__ = __name__
    form_fields = form.Fields(Iwwp_twitter_portlet)

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    __module__ = __name__
    form_fields = form.Fields(Iwwp_twitter_portlet)