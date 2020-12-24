# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/djangohelper/helper.py
# Compiled at: 2012-06-14 23:16:34
from django.http import HttpResponse
from django.utils import simplejson
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.conf import settings

def json_response(data):
    return HttpResponse(simplejson.dumps(data), mimetype='text/html')


def _ajax_login_required(msg):

    def decorator(view_func):

        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated():
                return json_response({'valid': False, 'msg': msg})
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator


def ajax_login_required(function=None, msg=_('please login first')):
    actual_decorator = _ajax_login_required(msg)
    if function:
        return actual_decorator(function)
    return actual_decorator


def flash_login_required(function):
    """
    Decorator to recognize a user  by its session.
    Used for Flash-Uploading.
    """

    def decorator(request, *args, **kwargs):
        try:
            engine = __import__(settings.SESSION_ENGINE, {}, {}, [''])
        except:
            import django.contrib.sessions.backends.db
            engine = django.contrib.sessions.backends.db

        session_data = engine.SessionStore(request.POST.get('session_key'))
        user_id = session_data['_auth_user_id']
        request.user = get_object_or_404(User, pk=user_id)
        return function(request, *args, **kwargs)

    return decorator


def request_get_next(request):
    """
    The part that's the least straightforward about views in this module is how they 
    determine their redirects after they have finished computation.

    In short, they will try and determine the next place to go in the following order:

    1. If there is a variable named ``next`` in the *POST* parameters, the view will
    redirect to that variable's value.
    2. If there is a variable named ``next`` in the *GET* parameters, the view will
    redirect to that variable's value.
    3. If Django can determine the previous page from the HTTP headers, the view will
    redirect to that previous page.
    """
    next = request.POST.get('next', request.GET.get('next', request.META.get('HTTP_REFERER', None)))
    if not next:
        next = request.path
    return next