# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/wsgiapptools/flash.py
# Compiled at: 2010-03-11 11:27:57
"""
"Flash" messaging support.

A "flash" message is a message displayed on a web page that is removed next
request.
"""
__all__ = [
 'add_message', 'get_messages', 'get_flash',
 'flash_middleware_factory']
import itertools, webob
from wsgiapptools import cookies
ENVIRON_KEY = 'wsgiapptools.flash'
COOKIE_NAME = 'flash'

def add_message(environ, message, type=None):
    """
    Add the flash message to the Flash manager in the WSGI environ."
    """
    return get_flash(environ).add_message(message, type)


def get_messages(environ):
    """
    Get the flasg messages from the Flash manager in the WSGI environ.
    """
    return get_flash(environ).get_messages()


def get_flash(environ):
    """
    Get the flash manager from the environ.
    """
    return environ[ENVIRON_KEY]


class Flash(object):
    """
    Flash message manager, associated with a WSGI environ.
    """

    def __init__(self, environ):
        self.request = webob.Request(environ)
        self.flashes = []

    def add_message(self, message, type=None):
        """
        Add a new flash message.

        Note: this can be called multiple times to set multiple messages. The
        messages can be retrieved, using get_messages below, and will be returned
        in the order they were added.
        """
        if type is None:
            type = ''
        self.flashes.append('%s:%s' % (type, message))
        return

    def get_messages(self):
        """
        Retrieve flash messages found in the request's cookies, returning them as a
        list of (type, message) tuples and deleting the cookies.
        """
        messages = []
        cookies_mgr = cookies.get_cookies(self.request.environ)
        for i in itertools.count():
            cookie_name = '%s.%d' % (COOKIE_NAME, i)
            message = self.request.cookies.get(cookie_name)
            if not message:
                break
            cookies_mgr.delete_cookie(cookie_name)
            (type, message) = message.split(':', 1)
            messages.append((type or None, message))

        return messages


def flash_middleware_factory(app):
    """
    Create a flash middleware WSGI application around the given WSGI
    application.
    """

    def middleware(environ, start_response):

        def _start_response(status, response_headers, exc_info=None):
            flash = environ[ENVIRON_KEY]
            cookies_mgr = cookies.get_cookies(environ)
            for (i, flash) in enumerate(flash.flashes):
                cookies_mgr.set_cookie(('%s.%d' % (COOKIE_NAME, i), flash))

            return start_response(status, response_headers, exc_info)

        environ[ENVIRON_KEY] = Flash(environ)
        return app(environ, _start_response)

    return middleware