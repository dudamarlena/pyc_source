# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/sendit/skin/page.py
# Compiled at: 2014-12-26 04:55:38
from urllib import quote
from zope.security.interfaces import Unauthorized
from ztfy.security.interfaces import ISecurityManager
from zope.traversing.browser.absoluteurl import absoluteURL
from ztfy.sendit.app.interfaces import ISenditApplication
from ztfy.skin.page import TemplateBasedPage
from ztfy.utils.traversing import getParent

class BaseSenditProtectedPage(object):
    """Base sendit protected page"""
    permission = 'ztfy.ViewSenditApplication'

    def __call__(self):
        security = ISecurityManager(self.context, None)
        if not security.canUsePermission(self.permission):
            app = getParent(self.context, ISenditApplication)
            self.request.response.redirect('%s/@@login.html?came_from=%s' % (absoluteURL(self.context, self.request),
             quote(absoluteURL(self, self.request), ':/')), trusted=app.trusted_redirects)
            raise Unauthorized
        return


class BaseSenditApplicationPage(BaseSenditProtectedPage, TemplateBasedPage):
    """Base sendit application page"""

    def __call__(self):
        try:
            BaseSenditProtectedPage.__call__(self)
        except Unauthorized:
            return ''

        return TemplateBasedPage.__call__(self)