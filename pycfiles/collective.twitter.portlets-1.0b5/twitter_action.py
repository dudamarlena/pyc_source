# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/twitter/action/twitter_action.py
# Compiled at: 2011-07-25 20:23:54
from persistent import Persistent
from OFS.SimpleItem import SimpleItem
from zope.interface import implements, Interface, alsoProvides
from zope.component import adapts
from zope.formlib import form
from zope import schema
from zope.schema.vocabulary import SimpleVocabulary
from z3c.form import interfaces
from zope.app.component.hooks import getSite
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from zope.component.interfaces import IObjectEvent
from plone.contentrules.rule.interfaces import IExecutable, IRuleElementData
from zope.schema.interfaces import IContextSourceBinder
from plone.app.contentrules.browser.formhelper import AddForm, EditForm
from Acquisition import aq_inner
from collective.twitter.action import MessageFactory as _
import twitter
from urllib import urlencode
from urllib2 import urlopen, HTTPError, URLError

def getTinyURL(url):
    """ returns shotend url or None """
    TINYURL = 'http://tinyurl.com/api-create.php'
    linkdata = urlencode(dict(url=url))
    try:
        link = urlopen(TINYURL, data=linkdata).read().strip()
    except URLError:
        link = None

    return link


def TwitterAccounts(context):
    registry = getUtility(IRegistry)
    accounts = registry['collective.twitter.accounts']
    return SimpleVocabulary.fromValues(accounts.keys())


alsoProvides(TwitterAccounts, IContextSourceBinder)

class ITwitterPublishAction(Interface):
    """ Twitter Config """
    tw_account = schema.Choice(title=_('Twitter account'), description=_('Which twitter account to use.'), required=True, source=TwitterAccounts)


class TwitterPublishAction(SimpleItem):
    """ 
    The actual persistent implementation of the action element.
    """
    implements(ITwitterPublishAction, IRuleElementData)
    tw_account = ''
    element = 'collective.twitter.action.TwitterPublishAction'

    @property
    def summary(self):
        return _('Twitter account: ${user}', mapping=dict(user=self.tw_account))


class TwitterPublishActionExecutor(object):
    """ 
    The executor for this action
    """
    implements(IExecutable)
    adapts(Interface, ITwitterPublishAction, IObjectEvent)

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def __call__(self):
        context = aq_inner(self.event.object)
        ploneutils = getToolByName(self.context, 'plone_utils')
        registry = getUtility(IRegistry)
        accounts = registry['collective.twitter.accounts']
        account = accounts.get(self.element.tw_account, {})
        if account:
            tw = twitter.Api(consumer_key=account.get('consumer_key'), consumer_secret=account.get('consumer_secret'), access_token_key=account.get('oauth_token'), access_token_secret=account.get('oauth_token_secret'))
            obj = self.event.object
            title = obj.Title()
            url = getTinyURL(obj.absolute_url())
            if url is None:
                return False
            twittertext = '%s\n%s' % (title[0:140 - (len(url) + 2)], url)
            try:
                status = tw.PostUpdate(twittertext)
                msg = _('Item published to twitter')
            except HTTPError, e:
                msg = _('Error while publishing to twitter %s' % str(e))
            except twitter.TwitterError, e:
                msg = _('Error while publishing to twitter %s' % str(e))
            else:
                ploneutils.addPortalMessage(msg)
                self.context.REQUEST.response.redirect(obj.absolute_url())
        else:
            msg = _('Could not publish to twitter, seems the account %s was removed from the list of authorized accounts for this site.' % self.element.tw_account)
            ploneutils.addPortalMessage(msg)
            self.context.REQUEST.response.redirect(obj.absolute_url())
        return True


class TwitterPublishActionAddForm(AddForm):
    """An add form for portal type conditions.
    """
    form_fields = form.FormFields(ITwitterPublishAction)
    label = _('Publish to Twitter action.')
    description = _('Publish a title and short URL to Twitter')
    form_name = _('Select account')

    def create(self, data):
        c = TwitterPublishAction()
        form.applyChanges(c, self.form_fields, data)
        return c


class TwitterPublishActionEditForm(EditForm):
    """An edit form for portal type conditions
    """
    form_fields = form.FormFields(ITwitterPublishAction)
    label = _('Edit publish to Twitter action.')
    description = _('Publish a title and short URL to Twitter')
    form_name = _('Select account')