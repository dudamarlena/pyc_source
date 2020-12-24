# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/jsl10n/browser/jstranslate.py
# Compiled at: 2010-02-10 04:59:04
__author__ = 'Richard Mitchell <richard.mitchell@isotoma.com>'
__docformat__ = 'restructuredtext en'
__version__ = '$Revision$'[11:-2]
import simplejson as json
from urllib import unquote
from zope.i18n import translate
from zope.i18nmessageid import MessageFactory
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

class JSTranslate(BrowserView):
    __module__ = __name__

    def __call__(self, *args, **kwargs):
        """ Returns JSON with translated strings for JavaScript using
            a Zope MessageFactory.
            
            Requests should be made either by GET or POST with the
            variables:
              * domain = the i18ndomain
              * msgid=default (where msgid is the msgid and default is the
                               default value)
        """
        if not hasattr(self, 'defaultdomain'):
            self.defaultdomain = 'hcpportal'
        if not hasattr(self, 'messagefactories'):
            self.messagefactories = {}
        domain = unquote(self.context.REQUEST.get('_jsl10n_domain', self.defaultdomain))
        _ = self.messagefactories.get(domain, self._addMessageFactory(domain))
        msgids = {}
        for id in self.context.REQUEST.form:
            if id not in ('_jsl10n_domain', '_jsl10n_lang'):
                msgids.update({unquote(id): unquote(self.context.REQUEST.form.get(id))})

        language_tool = getToolByName(self.context, 'portal_languages', None)
        target_language = unquote(self.context.REQUEST.get('_jsl10n_lang', language_tool is None and 'en' or language_tool.getPreferredLanguage()))
        for msgid in msgids:
            msgids[msgid] = translate(_(msgid, msgids[msgid]), target_language=target_language)

        self.context.REQUEST.response['mime-type'] = 'application/json'
        self.context.REQUEST.response.write(json.dumps(msgids))
        return

    def _addMessageFactory(self, domain):
        new_messagefactory = MessageFactory(domain)
        self.messagefactories.update({domain: new_messagefactory})
        return new_messagefactory