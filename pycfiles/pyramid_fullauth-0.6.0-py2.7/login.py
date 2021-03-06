# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyramid_fullauth/views/basic/login.py
# Compiled at: 2017-02-24 16:57:38
"""Authorisation related views."""
from pyramid.view import view_config
from pyramid.view import view_defaults
from pyramid.httpexceptions import HTTPSeeOther, HTTPRedirection
from pyramid.security import NO_PERMISSION_REQUIRED
from sqlalchemy.orm.exc import NoResultFound
from pyramid.compat import text_type
import pyramid_basemodel
from pyramid_fullauth.views import BaseView
from pyramid_fullauth.models import User
from pyramid_fullauth.events import BeforeLogIn
from pyramid_fullauth.events import AfterLogIn
from pyramid_fullauth.events import AlreadyLoggedIn

@view_defaults(route_name='login', permission=NO_PERMISSION_REQUIRED, renderer='pyramid_fullauth:resources/templates/login.mako')
class BaseLoginView(BaseView):
    """Basic logic for login views."""

    def __init__(self, request):
        """Prepare login views."""
        super(BaseLoginView, self).__init__(request)
        self.response = {'status': False, 
           'msg': self.request._('Login error', domain='pyramid_fullauth'), 
           'after': self.request.params.get('after', self.request.referer or '/'), 
           'csrf_token': self.request.session.get_csrf_token()}

    def _redirect_authenticated_user(self):
        """Redirect already logged in user away from login page."""
        redirect = HTTPSeeOther(location=self.response['after'])
        try:
            self.request.registry.notify(AlreadyLoggedIn(self.request))
        except HTTPRedirection as e_redirect:
            redirect = e_redirect

        if self.request.is_xhr:
            self.response['status'] = True
            self.response['msg'] = self.request._('Already logged in!', domain='pyramid_fullauth')
            self.response['after'] = redirect.location
            return self.response
        else:
            return redirect


@view_config(request_method='GET')
class LoginView(BaseLoginView):
    """Login view."""

    def __call__(self):
        """Display login page."""
        if self.request.authenticated_userid:
            return self._redirect_authenticated_user()
        else:
            self.request.registry.notify(BeforeLogIn(self.request, None))
            self.response['status'] = True
            del self.response['msg']
            return self.response


@view_config(request_method='POST', check_csrf=True)
@view_config(request_method='POST', check_csrf=True, xhr=True, renderer='json')
class LoginViewPost(BaseLoginView):
    """Login view POST method."""

    def __call__(self):
        """Login action."""
        if self.request.authenticated_userid:
            return self._redirect_authenticated_user()
        else:
            email = self.request.POST.get('email', '')
            password = self.request.POST.get('password', '')
            try:
                user = pyramid_basemodel.Session.query(User).filter(User.email == email).one()
                self.request.registry.notify(BeforeLogIn(self.request, user))
            except NoResultFound:
                self.request.registry.notify(BeforeLogIn(self.request, None))
                self.response['msg'] = self.request._('Wrong e-mail or password.', domain='pyramid_fullauth')
                return self.response
            except AttributeError as e:
                self.response['msg'] = text_type(e)
                return self.response

            if not user.check_password(password):
                self.response['msg'] = self.request._('Wrong e-mail or password.', domain='pyramid_fullauth')
                return self.response
            login_kwargs = {'remember_me': self.request.POST.get('remember')}
            try:
                self.request.registry.notify(AfterLogIn(self.request, user))
            except AttributeError as e:
                self.response['msg'] = text_type(e)
                return self.response
            except HTTPRedirection as redirect:
                login_kwargs['location'] = redirect.location

            redirect = self.request.login_perform(user, **login_kwargs)
            if self.request.is_xhr:
                self.response['status'] = True
                del self.response['msg']
                self.response['after'] = redirect.location
                return self.response
            return redirect