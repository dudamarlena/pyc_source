# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xbus/monitor/views/http_login.py
# Compiled at: 2016-06-27 04:20:00
# Size of source mod 2**32: 4329 bytes
from hashlib import sha1
from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember
from pyramid.security import forget
from pyramid.view import forbidden_view_config
from pyramid.response import Response
from xbus.monitor.models.monitor import DBSession
from xbus.monitor.models.monitor import User
from xbus.monitor.i18n import req_l10n

def setup(config):
    """helper to call during app configuration phase
    ie:  xbus.monitor:core.main

    :param config: the config instance for the running pyramid
    :return: Nothing
    """
    config.add_route('login', '/login')
    config.add_view(loginview, permission=NO_PERMISSION_REQUIRED, http_cache=0, renderer='xbus.monitor:templates/login.pt', route_name='login')
    config.add_route('logout', '/logout')
    config.add_view(logoutview, permission=NO_PERMISSION_REQUIRED, http_cache=0, route_name='logout')
    forbidden_view_config()(forbidden_view)


def loginview(request):
    """ this view is not decorated with the view_config decorator to avoid
    being always added because we only want it to be present when
    the configuration says we want http authentication using forms.

    The config.add_view is only added in the setup function which will be
    called from the application startup code, ie: xbus.monitor:core.main
    """
    _ = req_l10n(request)
    login_url = request.route_url('login')
    referrer = request.url
    if referrer == login_url:
        referrer = '/'
    came_from = request.params.get('came_from', referrer)
    login = ''
    password = ''
    message = _('Please log in before using this application')
    result = dict(page_title=_('Login'), message=message, url=request.route_url('login'), came_from=came_from, login=login, password=password)
    if 'form.submitted' in request.params:
        login = request.params['login']
        password = request.params['password']
        if not login or not password:
            return result
        password = password.encode('utf-8')
        db_session = DBSession()
        user = db_session.query(User).filter(User.user_name == login).first()
        if not user:
            return result
        user_pass = user.password.encode('utf-8')
        hashed_pass = sha1()
        hashed_pass.update(password + user_pass[:40])
        if user_pass[40:] != hashed_pass.hexdigest().encode('utf-8'):
            return result
        headers = remember(request, login)
        return HTTPFound(location=came_from, headers=headers)
    else:
        return result


def logoutview(request):
    """same as for login, we do not decorate the view because we want to
    manually add the view if and only if the http authentication is enabled
    see the setup function and where it is called: ie core.main()
    """
    headers = forget(request)
    login_url = request.route_url('login')
    return HTTPFound(location=login_url, headers=headers)


def forbidden_view(request):
    """this view will be used to redirect unlogged users to the login form
    and to display a real Forbidden to users that ARE logged but don't have
    access
    """
    _ = req_l10n(request)
    if request.authenticated_userid:
        return Response(_('You are not allowed'), status='401 Unauthorized')
    else:
        loc = request.route_url('login', _query=(('came_from', request.path),))
        return HTTPFound(location=loc)