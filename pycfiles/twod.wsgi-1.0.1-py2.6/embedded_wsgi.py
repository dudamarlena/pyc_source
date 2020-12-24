# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/twod/wsgi/embedded_wsgi.py
# Compiled at: 2011-06-28 10:17:42
"""
Utilities to use WSGI applications within Django.

"""
from Cookie import SimpleCookie
from twod.wsgi import TwodResponse
from twod.wsgi.exc import ApplicationCallError
__all__ = ('call_wsgi_app', 'make_wsgi_view')

def call_wsgi_app(wsgi_app, request, path_info):
    """
    Call the ``wsgi_app`` with ``request`` and return its response.
    
    :param wsgi_app: The WSGI application to be run.
    :type wsgi_app: callable
    :param request: The Django request.
    :type request: :class:`twod.wsgi.handler.TwodWSGIRequest`
    :param path_info: The ``PATH_INFO`` to be used by the WSGI application.
    :type path: :class:`basestring`
    :raises twod.wsgi.exc.ApplicationCallError: If ``path_info`` is not the
        last portion of the ``PATH_INFO`` in ``request``.
    :return: The response from the WSGI application, turned into a Django
        response.
    :rtype: :class:`twod.wsgi.TwodResponse`
    
    """
    new_request = request.copy()
    if not request.path_info.endswith(path_info):
        raise ApplicationCallError('Path %s is not the last portion of the PATH_INFO in the original request (%s)' % (
         path_info, request.path_info))
    consumed_path = request.path_info[:-len(path_info)]
    new_request.path_info = path_info
    new_request.script_name = request.script_name + consumed_path
    if request.user.is_authenticated():
        new_request.remote_user = request.user.username
    if 'wsgiorg.routing_args' in request.environ:
        del new_request.environ['wsgiorg.routing_args']
    if 'webob.adhoc_attrs' in request.environ:
        del new_request.environ['webob.adhoc_attrs']
    (status, headers, body) = new_request.call_application(wsgi_app)
    cookies = SimpleCookie()
    django_response = TwodResponse(body, status=status)
    for (header, value) in headers:
        if header.upper() == 'SET-COOKIE':
            if isinstance(value, unicode):
                value = value.encode('us-ascii')
            cookies.load(value)
        else:
            django_response[header] = value

    for (cookie_name, cookie) in cookies.items():
        cookie_attributes = {'key': cookie_name, 'value': cookie.value, 
           'max_age': cookie.get('max-age'), 
           'expires': cookie.get('expires'), 
           'path': cookie.get('path', '/'), 
           'domain': cookie.get('domain')}
        django_response.set_cookie(**cookie_attributes)

    return django_response


def make_wsgi_view(wsgi_app):
    """
    Return a callable which can be used as a Django view powered by the
    ``wsgi_app``.
    
    :param wsgi_app: The WSGI which will run the view.
    :return: The view callable.
    
    """

    def view(request, path_info):
        return call_wsgi_app(wsgi_app, request, path_info)

    return view