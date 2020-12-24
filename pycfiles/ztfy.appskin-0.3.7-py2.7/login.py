# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/appskin/login.py
# Compiled at: 2013-12-17 03:16:52
from httplib import UNAUTHORIZED
from z3c.form.interfaces import HIDDEN_MODE, IErrorViewSnippet
from zope.authentication.interfaces import IAuthentication
from zope.component.interfaces import ISite
from zope.publisher.interfaces.browser import IBrowserSkinType
from zope.security.interfaces import IUnauthorized
from zope.session.interfaces import ISession
from ztfy.appskin.interfaces import IApplicationBase, IApplicationResources, IAnonymousPage, ILoginView, ILoginViewHelp
from ztfy.skin.interfaces import IDefaultView
from z3c.form import field, button
from zope.component import queryMultiAdapter, getMultiAdapter, queryUtility, getUtilitiesFor
from zope.interface import implements, Interface, Invalid
from zope.publisher.skinnable import applySkin
from zope.schema import TextLine, Password
from zope.site import hooks
from zope.traversing.browser.absoluteurl import absoluteURL
from ztfy.skin.form import BaseAddForm
from ztfy.utils.traversing import getParent
from ztfy.appskin import _

class ILoginFormFields(Interface):
    """Login form fields interface"""
    username = TextLine(title=_('login-field', 'Login'), description=_('Principal ID'), required=True)
    password = Password(title=_('password-field', 'Password'), required=True)
    came_from = TextLine(title=_('camefrom-field', 'Login origin'), required=False)


def isUnauthorized(form):
    return IUnauthorized.providedBy(form.context)


class LoginView(BaseAddForm):
    """Main login view"""
    implements(ILoginView, IAnonymousPage)
    legend = _('Please enter valid credentials to login')
    css_class = 'login_view'
    icon_class = 'icon-lock'
    fields = field.Fields(ILoginFormFields)

    def __call__(self):
        if isUnauthorized(self):
            context, _action, _permission = self.context.args
            self.request.response.setStatus(UNAUTHORIZED)
        else:
            context = self.context
        self.app = getParent(context, IApplicationBase)
        return super(LoginView, self).__call__()

    @property
    def action(self):
        return '%s/@@login.html' % absoluteURL(self.app, self.request)

    @property
    def help(self):
        helper = queryMultiAdapter((self.context, self.request, self), ILoginViewHelp)
        if helper is not None:
            return helper.help
        else:
            return

    def update(self):
        super(LoginView, self).update()
        adapter = queryMultiAdapter((self.context, self.request, self), IApplicationResources)
        if adapter is None:
            adapter = queryMultiAdapter((self.context, self.request), IApplicationResources)
        if adapter is not None:
            for resource in adapter.resources:
                resource.need()

        return

    def updateWidgets(self):
        super(LoginView, self).updateWidgets()
        self.widgets['came_from'].mode = HIDDEN_MODE
        origin = self.request.get('came_from') or self.request.get(self.prefix + self.widgets.prefix + 'came_from')
        if not origin:
            origin = self.request.getURL()
            stack = self.request.getTraversalStack()
            if stack:
                origin += '/' + ('/').join(stack[::-1])
        self.widgets['came_from'].value = origin

    def updateActions(self):
        super(LoginView, self).updateActions()
        self.actions['login'].addClass('btn')

    def extractData(self, setErrors=True):
        data, errors = super(LoginView, self).extractData(setErrors=setErrors)
        if errors:
            self.logout()
            return (
             data, errors)
        else:
            self.request.form['login'] = data['username']
            self.request.form['password'] = data['password']
            self.principal = None
            context = getParent(self.context, ISite)
            while context is not None:
                old_site = hooks.getSite()
                try:
                    hooks.setSite(context)
                    for _name, auth in getUtilitiesFor(IAuthentication):
                        try:
                            self.principal = auth.authenticate(self.request)
                            if self.principal is not None:
                                return (data, errors)
                        except:
                            continue

                finally:
                    hooks.setSite(old_site)

                context = getParent(context, ISite, allow_context=False)

            if self.principal is None:
                error = Invalid(_('Invalid credentials'))
                view = getMultiAdapter((error, self.request, None, None, self, self.context), IErrorViewSnippet)
                view.update()
                errors += (view,)
                if setErrors:
                    self.widgets.errors = errors
                self.logout()
            return (
             data, errors)

    @button.buttonAndHandler(_('login-button', 'Login'), name='login')
    def handleLogin(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        else:
            if self.principal is not None:
                if isUnauthorized(self):
                    context, _action, _permission = self.context.args
                    self.request.response.redirect(absoluteURL(context, self.request))
                else:
                    came_from = data.get('came_from')
                    if came_from:
                        self.request.response.redirect(came_from)
                    else:
                        target = queryMultiAdapter((self.context, self.request, Interface), IDefaultView)
                        self.request.response.redirect('%s/%s' % (
                         absoluteURL(self.context, self.request),
                         target.viewname if target is not None else '@@index.html'))
                return ''
            self.request.response.redirect('%s/@@login.html?came_from=%s' % (absoluteURL(self.context, self.request),
             data.get('came_from')))
            return

    def logout(self):
        sessionData = ISession(self.request)['zope.pluggableauth.browserplugins']
        sessionData['credentials'] = None
        return


class LogoutView(BaseAddForm):
    """Main logout view"""

    def __call__(self):
        skin = queryUtility(IBrowserSkinType, self.context.getSkin())
        applySkin(self.request, skin)
        context = getParent(self.context, ISite)
        while context is not None:
            old_site = hooks.getSite()
            try:
                hooks.setSite(context)
                for _name, auth in getUtilitiesFor(IAuthentication):
                    auth.logout(self.request)

            finally:
                hooks.setSite(old_site)

            context = getParent(context, ISite, allow_context=False)

        target = queryMultiAdapter((self.context, self.request, Interface), IDefaultView)
        self.request.response.redirect('%s/%s' % (absoluteURL(self.context, self.request),
         target.viewname if target is not None else '@@SelectedManagementView.html'))
        return ''