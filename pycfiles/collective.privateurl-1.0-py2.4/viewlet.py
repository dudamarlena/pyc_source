# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/collective/privateurl/viewlet.py
# Compiled at: 2010-10-21 13:07:56
import re
from zExceptions import Unauthorized
from zope.component import getMultiAdapter
from Products.Five.browser import BrowserView
from plone.app.layout.viewlets.common import ViewletBase
whitelist = re.compile('require_login\\Z|login_form\\Z|mail_password_form\\Z|mail_password\\Z|passwordreset\\Z|pwreset_form\\Z|pwreset_finish\\Z')

class PrivateURL(ViewletBase):
    __module__ = __name__

    def update(self):
        self.portal_state = getMultiAdapter((self.context, self.request), name='plone_portal_state')

    def index(self):
        portal = self.portal_state.portal()
        if portal.hasProperty('privateurls'):
            if self.portal_state.anonymous() and whitelist.search(self.request.URL) is None:
                if portal.hasProperty('publicurls'):
                    for url in portal.publicurls:
                        if self.request.URL.startswith(url):
                            return ''

                for url in portal.privateurls:
                    if self.request.URL.startswith(url):
                        raise Unauthorized

        return ''