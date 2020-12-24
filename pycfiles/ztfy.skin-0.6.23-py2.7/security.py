# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/skin/security.py
# Compiled at: 2013-04-01 03:50:01
__docformat__ = 'restructuredtext'
from z3c.form.interfaces import HIDDEN_MODE
from z3c.json.interfaces import IJSONWriter
from zope.authentication.interfaces import IAuthentication, ILogout
from zope.component.interfaces import ISite
from zope.security.interfaces import IUnauthorized
from ztfy.skin.interfaces import IDefaultView, ILoginFormFields
from z3c.form import field, button
from z3c.formjs import ajax
from zope.component import adapts, queryMultiAdapter, getUtility, getUtilitiesFor, hooks
from zope.interface import implements
from zope.traversing.browser.absoluteurl import absoluteURL
from ztfy.skin.form import AddForm
from ztfy.utils.traversing import getParent
from ztfy.skin import _

class LogoutAdapter(object):
    adapts(IAuthentication)
    implements(ILogout)

    def __init__(self, auth):
        self.auth = auth

    def logout(self, request):
        return self.auth.logout(request)


class LoginLogoutView(ajax.AJAXRequestHandler):
    """Base login/logout view"""

    @ajax.handler
    def login(self):
        writer = getUtility(IJSONWriter)
        context = getParent(self.context, ISite)
        while context is not None:
            old_site = hooks.getSite()
            try:
                hooks.setSite(context)
                for _name, auth in getUtilitiesFor(IAuthentication):
                    if auth.authenticate(self.request) is not None:
                        return writer.write('OK')

            finally:
                hooks.setSite(old_site)

            context = getParent(context, ISite, allow_context=False)

        return writer.write('NOK')

    @ajax.handler
    def logout(self):
        writer = getUtility(IJSONWriter)
        context = getParent(self.context, ISite)
        while context is not None:
            old_site = hooks.getSite()
            try:
                hooks.setSite(context)
                for _name, auth in getUtilitiesFor(IAuthentication):
                    if auth.logout(self.request):
                        return writer.write('OK')

            finally:
                hooks.setSite(old_site)

            context = getParent(context, ISite, allow_context=False)

        return writer.write('NOK')


class LoginForm(AddForm):
    """ZMI login form"""
    title = _('Login form')
    legend = _('Please enter valid credentials to login')
    fields = field.Fields(ILoginFormFields)

    def __call__(self):
        self.request.response.setStatus(401)
        return super(LoginForm, self).__call__()

    def updateWidgets(self):
        super(LoginForm, self).updateWidgets()
        self.widgets['came_from'].mode = HIDDEN_MODE
        if IUnauthorized.providedBy(self.context):
            self.widgets['came_from'].value = self.request.getURL()

    @button.buttonAndHandler(_('login-button', 'Login'))
    def handleLogin(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        else:
            self.request.form['login'] = data['username']
            self.request.form['password'] = data['password']
            if IUnauthorized.providedBy(self.context):
                context, _layer, _permission = self.context.args
            else:
                context = self.context
            site = getParent(context, ISite)
            while site is not None:
                old_site = hooks.getSite()
                try:
                    hooks.setSite(site)
                    for _name, auth in getUtilitiesFor(IAuthentication):
                        if auth.authenticate(self.request) is not None:
                            target = data.get('came_from')
                            if target:
                                self.request.response.redirect(target)
                            else:
                                target = queryMultiAdapter((context, self.request, self), IDefaultView)
                                if target is not None:
                                    self.request.response.redirect(target.getAbsoluteURL())
                                else:
                                    self.request.response.redirect('%s/@@SelectedManagementView.html' % absoluteURL(self.context, self.request))
                                return ''

                finally:
                    hooks.setSite(old_site)

                site = getParent(site, ISite, allow_context=False)

            return