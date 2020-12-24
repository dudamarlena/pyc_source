# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/fourdigits/portlet/twitter/fourdigitsportlettwitter.py
# Compiled at: 2011-10-24 09:38:37
from zope.interface import implements
from zope import schema
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from fourdigits.portlet.twitter import FourdigitsPortletTwitterMessageFactory as _
from fourdigits.portlet.twitter import twitter
import re
from urllib2 import URLError
from plone.memoize.compress import xhtml_compress
urlsRegexp = re.compile("\n    (\n    # Protocol\n    http://\n    # Alphanumeric, dash, slash or dot\n    [A-Za-z0-9\\-/?=&.]*\n    # Don't end with a dot\n    [A-Za-z0-9\\-/]+\n    )\n    ", re.VERBOSE)
hashRegexp = re.compile('\n    # Hash at start of string or after space, followed by at least one\n    # alphanumeric or dash\n    (?:^|(?<=\\s))\\#([A-Za-z0-9\\-]+)\n    ', re.VERBOSE)
atRegexp = re.compile('\n    # At symbol at start of string or after space, followed by at least one\n    # alphanumeric or dash\n    (?:^|(?<=\\s))@([A-Za-z0-9\\-]+)\n    ', re.VERBOSE)
emailRegexp = re.compile('\n    # Email at start of string or after space\n    (?:^|(?<=\\s))([A-Z0-9._%+-]+@[A-Z0-9.-]+\\.[A-Z]{2,4})\\b\n    ', re.VERBOSE | re.IGNORECASE)

def expand_tweet(str):
    """This method takes a string, parses it for URLs, hashtags and mentions
       and returns a hyperlinked string."""
    str = re.sub(urlsRegexp, '<a href="\\g<1>">\\g<1></a>', str)
    str = re.sub(hashRegexp, '<a href="http://twitter.com/search?q=%23\\g<1>">#\\g<1></a>', str)
    str = re.sub(atRegexp, '<a href="http://twitter.com/\\g<1>">@\\g<1></a>', str)
    str = re.sub(emailRegexp, '<a href="mailto:\\g<1>">\\g<1></a>', str)
    return str


class IFourdigitsPortletTwitter(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """
    __module__ = __name__
    name = schema.TextLine(title=_('Title'), description=_('The title of the portlet'))
    username = schema.TextLine(title=_('Username'), description=_('The tweets of this user will be shown'), required=False)
    userinfo = schema.Bool(title=_('Show user info?'), description=_('Show info of the Twitter user?'), required=False)
    includerts = schema.Bool(title=_('Include retweets'), description=_("Include retweets of the user's account?"), required=False, default=True)
    search = schema.Text(title=_('Search'), description=_('The tweets containing this text will be shown enter one per line, hashtags are allowed'), required=False)
    filtertext = schema.Text(title=_('Filtertext'), description=_('If a message containes (curse) words in the filtertext it wont be shown, one per line'), required=False)
    userdisplay = schema.Int(title=_('Number of items to display based on the username'), description=_('How many items to list based on the username.'), required=False, default=5)
    searchdisplay = schema.Int(title=_('Number of items to display based on the searchtext'), description=_('How many items to list based on the searchtext.'), required=False, default=5)
    searchlimit = schema.Int(title=_('Number of items to search for, defaults to 40'), description=_('Number of items to search for, defaults to 40'), required=True, default=40)
    language = schema.Text(title=_('Languagefilter'), description=_('Language ISO code for the tweets (e.g.: en, nl, fr), if you like to filter on language one per line'), required=False)
    userpictures = schema.Bool(title=_('Show user pictures?'), description=_('Should the portlet show the twitter user pictures?'), default=True)


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """
    __module__ = __name__
    implements(IFourdigitsPortletTwitter)
    includerts = True
    userinfo = True

    def __init__(self, name='', username='', search='', filtertext='', userdisplay=5, searchdisplay=5, searchlimit=40, language='', userpictures=False, includerts=True, userinfo=False):
        self.name = name
        self.username = username
        self.search = search
        self.filtertext = filtertext
        self.userdisplay = userdisplay
        self.searchdisplay = searchdisplay
        self.searchlimit = searchlimit
        self.language = language
        self.userpictures = userpictures
        self.includerts = includerts
        self.userinfo = userinfo

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return 'fourdigits.portlet.twitter'


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """
    __module__ = __name__
    _template = ViewPageTemplateFile('fourdigitsportlettwitter.pt')
    twapi = twitter.Api()

    def render(self):
        return xhtml_compress(self._template())

    @property
    def title(self):
        return self.data.name or _('Tweets')

    @property
    def available(self):
        return True

    def expand(self, str):
        return expand_tweet(str)

    def showuserinfo(self):
        """Should we show userinfo"""
        if self.data.userinfo:
            return True
        return False

    def getuserinfo(self):
        """Get twitter user info"""
        userinfo = self.twapi.GetUser(self.data.username)
        return userinfo

    def twittermessages(self):
        """Twitter messages"""
        return self._data()

    def _data(self):
        return self.gettweets()

    def gettweetsofuser(self, username, userpictures, includerts):
        """Return the tweets of a certain user"""
        try:
            tweets = self.twapi.GetUserTimeline(username, include_rts=includerts, include_entities=True)
        except URLError:
            tweets = []

        return tweets

    def gettweetsbysearch(self, searchterms, searchlimit, language):
        """Return tweets based on a search query"""
        searchterms = searchterms.encode('utf-8')
        searchterms = searchterms.split('\n')
        for searchterm in searchterms:
            try:
                tweets = self.twapi.GetSearch(term=searchterm, per_page=searchlimit, lang=language)
            except:
                tweets = []

        return tweets

    def gettweets(self):
        """Get the tweets and filter them"""
        username = self.data.username
        searchterms = self.data.search
        userdisplay = self.data.userdisplay
        searchdisplay = self.data.searchdisplay
        searchlimit = self.data.searchlimit
        filtertext = self.data.filtertext
        languages = self.data.language
        userpictures = self.data.userpictures
        includerts = self.data.includerts
        results = []
        tweets = []
        if username:
            tweets = self.gettweetsofuser(username, userpictures, includerts)
        tweets = tweets[:userdisplay]
        searchresults = []
        if searchterms:
            if languages:
                languages = languages.split('\n')
                for lang in languages:
                    lang = str(lang.encode('utf-8'))
                    searchresults += self.gettweetsbysearch(searchterms, searchlimit, language=lang)

            else:
                searchresults += self.gettweetsbysearch(searchterms, searchlimit, language='')
            filtered_results = [ tweet for tweet in searchresults if tweet not in tweets ]
            tweets += filtered_results[:searchdisplay]
        if filtertext:
            filtertext = filtertext.lower()
            filterlist = filtertext.split('\n')
        for tweet in tweets:
            tweet.username = tweet.user.GetScreenName()
            picture = tweet.user.GetProfileImageUrl()
            tweet.author_url = 'http://twitter.com/%s' % tweet.username
            if userpictures:
                tweet.picture = picture
            usernameLength = len(tweet.username) + 1
            if tweet.text[0:usernameLength] == tweet.username + ':':
                tweet.text = tweet.text[usernameLength:len(tweet.text)]
            if filtertext:
                text = tweet.text.lower()
                if not [ 1 for x in filterlist if x in text ]:
                    results.append(tweet)
            else:
                results.append(tweet)

        tweets = results
        tweets.sort(key=lambda tweet: tweet.GetCreatedAtInSeconds())
        tweets.reverse()
        return tweets


class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    __module__ = __name__
    form_fields = form.Fields(IFourdigitsPortletTwitter)
    label = _('Twitter portlet')
    description = _('This portlet displays tweets. Please keep note that some settings will apply after 5 minutes.')

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    __module__ = __name__
    form_fields = form.Fields(IFourdigitsPortletTwitter)
    label = _('Twitter portlet')
    description = _('This portlet displays tweets. Please keep note that some settings will apply after 5 minutes.')