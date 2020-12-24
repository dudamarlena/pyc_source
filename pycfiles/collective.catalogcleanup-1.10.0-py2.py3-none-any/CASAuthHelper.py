# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/cas4plone/CASAuthHelper.py
# Compiled at: 2011-01-21 06:21:44
__doc__ = ''
from HTMLParser import HTMLParseError
import urllib
from zLOG import LOG, INFO
from AccessControl.SecurityInfo import ClassSecurityInfo
from OFS.PropertyManager import PropertyManager
from App.class_init import default__class_init__ as InitializeClass
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.utils import classImplements
from Products.PluggableAuthService.interfaces.plugins import IExtractionPlugin, IChallengePlugin, IAuthenticationPlugin, ICredentialsResetPlugin
from CASXMLResponseParser import CASXMLResponseParser
try:
    from Products.CMFPlone.factory import _IMREALLYPLONE4
    PLONE40 = True
except ImportError:
    PLONE40 = False

addCASAuthHelperForm = PageTemplateFile('zmi/addCASAuthHelperForm.zpt', globals())

def addCASAuthHelper(dispatcher, id, title=None, REQUEST=None):
    """ Add a CASAuthHelper to a Pluggable Auth Service. """
    sp = CASAuthHelper(id, title)
    dispatcher._setObject(sp.getId(), sp)
    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect('%s/manage_workspace?manage_tabs_message=CASAuthHelper+added.' % dispatcher.absolute_url())
    return


class CASAuthHelper(PropertyManager, BasePlugin):
    """ Multi-plugin for managing details of CAS Authentication. """
    meta_type = 'CAS Auth Helper'
    login_url = 'https://your.cas.server:port/cas/login'
    logout_url = 'https://your.cas.server:port/cas/logout'
    validate_url = 'https://your.cas.server:port/cas/validate'
    session_var = '__ac'
    use_ACTUAL_URL = True
    security = ClassSecurityInfo()
    _properties = (
     {'id': 'title', 'label': 'Title', 
        'type': 'string', 
        'mode': 'w'},
     {'id': 'login_url', 'label': 'CAS Login URL', 
        'type': 'string', 
        'mode': 'w'},
     {'id': 'logout_url', 'label': 'CAS Logout URL', 
        'type': 'string', 
        'mode': 'w'},
     {'id': 'validate_url', 'type': 'string', 
        'label': 'Ticket validation URL', 
        'mode': 'w'},
     {'id': 'session_var', 'type': 'string', 
        'label': 'Session credentials id', 
        'mode': 'w'},
     {'id': 'use_ACTUAL_URL', 'type': 'boolean', 
        'label': 'Use ACTUAL_URL instead of URL', 
        'mode': 'w'})
    manage_options = BasePlugin.manage_options[:1] + PropertyManager.manage_options + BasePlugin.manage_options[2:]

    def __init__(self, id, title=None):
        self._setId(id)
        self.title = title

    security.declarePrivate('extractCredentials')

    def extractCredentials(self, request):
        """ Extract credentials from session or 'request'. """
        creds = {}
        username = None
        if self.session_var not in request:
            ticket = request.form.get('ticket')
            if ticket is None:
                return creds
            username = self.validateTicket(self.getService(request), ticket)
            if username is None:
                return creds
            if PLONE40:
                self.session._setupSession(username, request.response)
                creds['login'] = username
                return creds
            cookie = self.session.source.createIdentifier(username)
            creds['login'] = username
            creds['cookie'] = cookie
            creds['source'] = 'plone.session'
            self.session.setupSession(username, request.response)
            return creds
        return creds

    def validateTicket(self, service, ticket):
        checkparams = '?service=' + service + '&ticket=' + ticket
        casdata = urllib.URLopener().open(self.validate_url + checkparams)
        test = casdata.readline().strip()
        if test == 'yes':
            username = casdata.readline().strip()
            return username
        else:
            if test.lower().find('cas:serviceresponse') > 0:
                try:
                    parser = CASXMLResponseParser()
                    while test:
                        parser.feed(test)
                        if parser.getUser():
                            return parser.getUser()
                        test = casdata.readline()

                    if parser.getFailure():
                        LOG('CAS4PAS', INFO, 'Cannot validate ticket: %s [service=%s]' % (
                         parser.getFailure(), service))
                    else:
                        LOG('CAS4PAS', INFO, "CASXMLResponseParser couldn't understand CAS server response")
                except HTMLParseError, e:
                    LOG('CAS4PAS', INFO, 'Error parsing ticket validation response: ' + str(e))

                return
            else:
                LOG('CAS4PAS', INFO, 'ticket validation: some unknown authentication error occurred')
                return
            return

    def authenticateCredentials(self, credentials):
        if credentials['extractor'] != self.getId():
            return (None, None)
        else:
            username = credentials['login']
            return (
             username, username)

    security.declarePrivate('challenge')

    def challenge(self, request, response, **kw):
        """ Challenge the user for credentials. """
        session = self.REQUEST.SESSION
        session[self.session_var] = None
        if request.has_key('ticket'):
            return 0
        else:
            url = self.getLoginURL()
            if url:
                service = self.getService(request)
                response.redirect('%s?service=%s' % (url, service), lock=1)
                return 1
            return 0

    security.declarePrivate('resetCredentials')

    def resetCredentials(self, request, response):
        """ Clears credentials and redirects to CAS logout page"""
        session = self.REQUEST.SESSION
        session[self.session_var] = None
        if self.logout_url:
            self.REQUEST.RESPONSE.redirect(self.logout_url)
        return

    security.declarePrivate('getLoginURL')

    def getLoginURL(self):
        """ Where to send people for logging in """
        return self.login_url

    def getService(self, request):
        """extract urlencoded service URL from REQUEST and remove the ticket from
        GET parameters
        This function handles GET parameters
        """
        if self.use_ACTUAL_URL:
            service = request.get('ACTUAL_URL', request['URL'])
        else:
            service = request['URL']
        query_string = request.get('QUERY_STRING', '')
        ticket_idx = query_string.find('ticket=')
        if ticket_idx > 1:
            query_string = query_string[:ticket_idx - 1]
        elif ticket_idx == 0:
            query_string = ''
        if query_string:
            service = '%s?%s' % (service, query_string)
        return urllib.quote(service)


classImplements(CASAuthHelper, IExtractionPlugin, IChallengePlugin, ICredentialsResetPlugin, IAuthenticationPlugin)
InitializeClass(CASAuthHelper)