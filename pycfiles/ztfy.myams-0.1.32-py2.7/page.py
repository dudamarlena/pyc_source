# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/myams/page.py
# Compiled at: 2014-10-07 05:36:39
from datetime import datetime
from persistent.interfaces import IPersistent
from z3c.json.interfaces import IJSONWriter
from z3c.template.interfaces import ILayoutTemplate
from zope.authentication.interfaces import IAuthentication
from zope.pagetemplate.interfaces import IPageTemplate
from zope.security.interfaces import IUnauthorized
from ztfy.myams.interfaces import IInnerPage, IModalPage
from z3c.template.template import getPageTemplate, getLayoutTemplate
from zope.component import getMultiAdapter, getUtility
from zope.i18n import translate
from zope.interface import implements
from zope.publisher.browser import BrowserPage
from zope.traversing.browser.absoluteurl import absoluteURL
from ztfy.utils.date import formatDatetime
from ztfy.utils.text import textToHTML
from ztfy.utils.timezone import tztime
from ztfy.utils.traversing import getParent
from ztfy.myams import _

class BaseTemplateBasedPage(BrowserPage):
    """Base template based page"""
    template = getPageTemplate()

    def __call__(self):
        self.update()
        return self.render()

    def update(self):
        pass

    def render(self):
        if self.template is None:
            template = getMultiAdapter((self, self.request), IPageTemplate)
            return template(self)
        else:
            return self.template()


class TemplateBasedPage(BaseTemplateBasedPage):
    """Template based page"""
    layout = getLayoutTemplate()

    def __call__(self):
        self.update()
        if self.layout is None:
            layout = getMultiAdapter((self, self.request), ILayoutTemplate)
            return layout(self)
        else:
            return self.layout()


class BaseIndexPage(TemplateBasedPage):
    """Base index page"""
    pass


class InnerPage(TemplateBasedPage):
    """Inner page"""
    implements(IInnerPage)


class ModalPage(TemplateBasedPage):
    """Modal page"""
    implements(IModalPage)


class ExceptionView(BrowserPage):
    """Base exception view"""

    @property
    def error_name(self):
        return self.context.__class__.__name__

    @property
    def error_message(self):
        return textToHTML(translate(getattr(self.context, 'message', ''), context=self.request) or ('\n').join(str(arg) for arg in self.context.args), request=self.request)

    @property
    def error_datetime(self):
        return formatDatetime(tztime(datetime.utcnow()))

    @property
    def error_user(self):
        principal = self.request.principal
        return '%s (%s)' % (principal.title, principal.id)

    def __call__(self):
        self.request.response.setStatus(500)
        writer = getUtility(IJSONWriter)
        return writer.write({'status': 'messagebox', 'messagebox': {'status': 'error', 'title': translate(_('An error occurred: %s'), context=self.request) % self.error_name, 
                          'content': self.error_message, 
                          'number': self.error_datetime, 
                          'icon': 'fa fa-warning animated shake'}})


class UnauthorizedExceptionView(ExceptionView):
    """Unauthorized exception view"""

    def __call__(self):
        principal = self.request.principal
        auth = getUtility(IAuthentication)
        auth.unauthorized(principal.id, self.request)
        try:
            context = self.context.args[0]
        except:
            context = self.context

        self.request.response.setStatus(200)
        if '/@@ajax/' in self.request.getURL() or self.request.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            parent = getParent(context, IPersistent)
            writer = getUtility(IJSONWriter)
            return writer.write({'status': 'modal', 'location': 'login-dialog.html?came_from=%s' % absoluteURL(parent, self.request)})
        self.request.response.redirect('login.html?came_from=%s' % absoluteURL(context, self.request))