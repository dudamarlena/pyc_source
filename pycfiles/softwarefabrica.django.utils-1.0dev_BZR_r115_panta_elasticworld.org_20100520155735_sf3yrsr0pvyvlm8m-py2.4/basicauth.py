# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/softwarefabrica/django/utils/basicauth.py
# Compiled at: 2009-10-12 06:16:24
import base64
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
import logging

def view_or_basicauth(view, request, test_func, realm='', *args, **kwargs):
    """
    This is a helper function used by both 'logged_in_or_basicauth' and
    'has_perm_or_basicauth' that does the nitty of determining if they
    are already logged in or if they have provided proper http-authorization
    and returning the view if all goes well, otherwise responding with a 401.
    """
    if test_func(request.user):
        logging.debug('view_or_basicauth: already logged')
        return view(request, *args, **kwargs)
    if 'HTTP_AUTHORIZATION' in request.META:
        logging.info('HTTP_AUTHORIZATION in request')
        auth = request.META['HTTP_AUTHORIZATION'].split()
        logging.debug('HTTP_AUTHORIZATION is %s' % repr(auth))
        if len(auth) == 2:
            if auth[0].lower() == 'basic':
                (uname, passwd) = base64.b64decode(auth[1]).split(':')
                user = authenticate(username=uname, password=passwd)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        request.user = user
                        return view(request, *args, **kwargs)
    logging.debug('HTTP auth failed')
    response = HttpResponse()
    response.status_code = 401
    response['WWW-Authenticate'] = 'Basic realm="%s"' % realm
    return response


def logged_in_or_basicauth(realm=''):
    """
    A simple decorator that requires a user to be logged in. If they are not
    logged in the request is examined for a 'authorization' header.

    If the header is present it is tested for basic authentication and
    the user is logged in with the provided credentials.

    If the header is not present a http 401 is sent back to the
    requestor to provide credentials.

    The purpose of this is that in several django projects I have needed
    several specific views that need to support basic authentication, yet the
    web site as a whole used django's provided authentication.

    The uses for this are for urls that are access programmatically such as
    by rss feed readers, yet the view requires a user to be logged in. Many rss
    readers support supplying the authentication credentials via http basic
    auth (and they do NOT support a redirect to a form where they post a
    username/password.)

    Use is simple:

    @logged_in_or_basicauth()
    def your_view:
        ...

    You can provide the name of the realm to ask for authentication within.
    """

    def view_decorator(func):

        def wrapper(request, *args, **kwargs):
            return view_or_basicauth(func, request, (lambda u: u.is_authenticated()), realm, *args, **kwargs)

        return wrapper

    return view_decorator


def has_perm_or_basicauth(perm, realm=''):
    """
    This is similar to the above decorator 'logged_in_or_basicauth'
    except that it requires the logged in user to have a specific
    permission.

    Use:

    @logged_in_or_basicauth('asforums.view_forumcollection')
    def your_view:
        ...

    """

    def view_decorator(func):

        def wrapper(request, *args, **kwargs):
            return view_or_basicauth(func, request, (lambda u: u.has_perm(perm)), realm, *args, **kwargs)

        return wrapper

    return view_decorator