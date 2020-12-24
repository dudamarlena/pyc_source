# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/collective/linkedin/browser/interfaces.py
# Compiled at: 2010-04-13 18:59:51
from zope import schema
from zope.interface import Interface
from plone.theme.interfaces import IDefaultPloneLayer
from plone.portlets.interfaces import IPortletDataProvider
from plone.portlet.static.static import IStaticPortlet
from collective.linkedin import LinkedInMessageFactory as _

class IThemeSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer.
    """
    __module__ = __name__


class ICollectiveLinkedInManagement(Interface):
    """
    """
    __module__ = __name__
    company_insider_widget = schema.TextLine(title=_('Company Insider Widget'), required=False, description=_('Enter the company name'))
    action_popup = schema.Bool(title=_('Site action pop up'), required=False, description=_('Check it if you want the site action popup'))
    border = schema.Bool(title=_('Border'), required=False, description=_('Caution: if you enable popup, this needs to be checked.'))
    api_key = schema.TextLine(title=_('Linkedin Api Key'), required=False, description=_('Api Key obtained from linkedin at https://www.linkedin.com/secure/developer'))
    secret_key = schema.TextLine(title=_('Linkedin Secret Key'), required=False, description=_('Secret Key obtained from linkedin along with API key'))
    request_token = schema.TextLine(title=_('Linkedin generated Request Token'), required=False, description=_('Api Generated Key obtained from linkedin after running Generate Credentials'))
    request_token_secret = schema.TextLine(title=_('Linkedin generated Request Token Secret'), required=False, description=_('Secret Generated Key obtained from linkedin after running Generate Credentials'))
    access_token = schema.TextLine(title=_('Linkedin generated Access Token'), required=False, description=_('Api Generated Token obtained from linkedin after running Generate Credentials'))
    access_token_secret = schema.TextLine(title=_('Linkedin generated Access Token Secret'), required=False, description=_('Secret Generated Token obtained from linkedin after running Generate Credentials'))
    verification_number = schema.TextLine(title=_('Verification number'), required=False, description=_('Verification number obtained from Generate Credentials process.'))


class ILinkedinTool(Interface):
    """
    """
    __module__ = __name__

    def get_user_profile(self, user_profile_url):
        pass

    def set_user_pic_from_linkedin(self, user):
        pass


class ICompanyInfoPortlet(IStaticPortlet):
    """ Defines a new portlet "Company Info" which takes properties of the existing static text portlet. """
    __module__ = __name__


class IProfileInfoPortlet(IPortletDataProvider):
    """ Defines a new portlet "Profile Info" """
    __module__ = __name__
    profile_id = schema.TextLine(title=_('LinkedIn user id'), description=_('Id of the LinkedIn user to show information'), default='', required=True)
    name = schema.TextLine(title=_('LinkedIn Name'), description=_('The name of the person'), default='', required=True)