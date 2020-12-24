# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.6/dist-packages/queries/views/decorators.py
# Compiled at: 2010-05-09 07:06:47
import base64
try:
    from functools import wraps
except ImportError:
    from django.utils.functional import wraps

from django import http, template
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render_to_response
from django.utils.translation import ugettext_lazy, ugettext as _
ERROR_MESSAGE = ugettext_lazy('Please enter a correct username and password. Note that both fields are case-sensitive.')
LOGIN_FORM_KEY = 'this_is_the_login_form'

def _display_login_form(request, error_message=''):
    request.session.set_test_cookie()
    return render_to_response('query/login.html', {'title': _('Log in'), 
       'app_path': request.get_full_path(), 
       'error_message': error_message}, context_instance=template.RequestContext(request))


def staff_member_required(view_func):
    """
    Decorator for views that checks that the user is logged in and is a staff
    member, displaying the login page if necessary.
    """

    def _checklogin(request, *args, **kwargs):
        if request.user.is_authenticated() and request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            assert hasattr(request, 'session'), "The Django query requires session middleware to be installed. Edit your MIDDLEWARE_CLASSES setting to insert 'django.contrib.sessions.middleware.SessionMiddleware'."
            if LOGIN_FORM_KEY not in request.POST:
                if request.POST:
                    message = _('Please log in again, because your session has expired.')
                else:
                    message = ''
                return _display_login_form(request, message)
            if not request.session.test_cookie_worked():
                message = _("Looks like your browser isn't configured to accept cookies. Please enable cookies, reload this page, and try again.")
                return _display_login_form(request, message)
            request.session.delete_test_cookie()
            username = request.POST.get('username', None)
            password = request.POST.get('password', None)
            user = authenticate(username=username, password=password)
            if user is None:
                message = ERROR_MESSAGE
                if '@' in username:
                    users = list(User.objects.filter(email=username))
                    if len(users) == 1 and users[0].check_password(password):
                        message = _("Your e-mail address is not your username. Try '%s' instead.") % users[0].username
                    else:
                        message = _("Usernames cannot contain the '@' character.")
                return _display_login_form(request, message)
            if user.is_active and user.is_staff:
                login(request, user)
                return http.HttpResponseRedirect(request.get_full_path())
            return _display_login_form(request, ERROR_MESSAGE)
            return

    return wraps(view_func)(_checklogin)