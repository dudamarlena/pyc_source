# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/sylvester/browser/interfaces.py
# Compiled at: 2009-07-12 07:00:21
from zope.interface import Interface
from zope.viewlet.interfaces import IViewletManager

class ITwitterAPI(Interface):
    """
    Interface for python-twitter API
    """
    __module__ = __name__


class ITwitterCredentialsProvider(Interface):
    """
    Interface for adapter which provides twitter credentials
    """
    __module__ = __name__

    def username():
        """
        Return twitter username
        """
        pass

    def password():
        """
        Return twitter password
        """
        pass


class ISylvesterView(Interface):
    """
    Interface
    """
    __module__ = __name__

    def authenticate(redirect=False):
        """
        Call redirect_to_credentials_form if _setup_twitter_adapter returns 
        False.
        """
        pass

    def redirect_to_credentials_form():
        """
        Redirect to page where user can enter credentials for this session.
        """
        pass

    def _setup_twitter_adapter():
        """
        Set up attribute on the view which carries authentication information.
        Return True if member can authenticate to twitter, False otherwise
        """
        pass

    def linkify(text):
        """
        Replace occurences of URI's in text with proper markup. Return the
        transformed text.
        """
        pass

    def format_ago(atime, uppercase=False, invert=False):
        """        
        Return a relative translated time string, eg. "4 hours ago" or
        "10 minutes ago".

        This method takes into account that the Zope server and the browser 
        may be in different timezones.

        atime: a parsable date string
        """
        pass

    def latest():
        """
        Return the latest status update by the authenticated member
        """
        pass

    def getPluggableViewlets():
        """
        Return viewlets that can be plugged into the dashboard
        """
        pass


class ICredentialsFormView(Interface):
    """
    Interface
    """
    __module__ = __name__

    def name():
        """
        Return name that browser view is registered with in ZCML
        """
        pass

    def submit(username, password, came_from=''):
        """
        Handle form submission
        """
        pass


class IPublishToTwitterFormView(Interface):
    """
    Interface
    """
    __module__ = __name__

    def name():
        """
        Return name that browser view is registered with in ZCML
        """
        pass

    def submit(came_from=''):
        """
        Handle form submission
        """
        pass


class ISylvesterDashboardManager(IViewletManager):
    """ 
    Render dashboard
    """
    __module__ = __name__


class ISylvesterStatusletManager(IViewletManager):
    """ 
    Render a status
    """
    __module__ = __name__


class ISylvesterFriendletManager(IViewletManager):
    """ 
    Render a friend
    """
    __module__ = __name__