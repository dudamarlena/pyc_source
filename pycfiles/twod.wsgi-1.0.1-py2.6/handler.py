# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/twod/wsgi/handler.py
# Compiled at: 2011-06-28 10:17:42
"""
Django request/response handling a la WSGI.

"""
from webob import Request
from django.core.handlers.wsgi import WSGIRequest, WSGIHandler
from django.http import HttpResponse
__all__ = ('TwodWSGIRequest', 'TwodResponse', 'DjangoApplication')
_ACTUAL_REASON_HEADER = 'X-Actual-Status-Reason'

class TwodWSGIRequest(WSGIRequest, Request):
    """
    Pythonic proxy for the WSGI environment.
    
    This class is the Django request extended by WebOb's request. Where they
    both have the same members, Django's take precedence. For example, ``.GET``
    uses :attr:`django.core.handlers.wsgi.WSGIRequest.GET` instead of
    :attr:`webob.Request.GET`.
    
    To access WebOb's GET and POST dictionaries, you have to use ``.uGET``
    and ``.uPOST`` respectively.
    
    """
    environ = None
    path = None
    method = None
    META = None

    def __init__(self, environ):
        Request.__init__(self, environ)
        WSGIRequest.__init__(self, environ)

    uPOST = Request.POST
    uGET = Request.GET

    @property
    def str_POST(self):
        """
        Return the POST arguments by using WebOb.
        
        """
        original_content_length = self.environ.get('CONTENT_LENGTH')
        try:
            return super(TwodWSGIRequest, self).str_POST
        finally:
            self.environ['CONTENT_LENGTH'] = original_content_length
            self._seek_input()

    def _load_post_and_files(self):
        """
        Parse the POST arguments and uploaded files by using Django.
        
        """
        try:
            return super(TwodWSGIRequest, self)._load_post_and_files()
        finally:
            self._seek_input()

    def _seek_input(self):
        if 'wsgi.input' in self.environ:
            self.environ['wsgi.input'].seek(0)


class TwodResponse(HttpResponse):
    """
    Django-based response class which keeps the HTTP status reason phrase.
    
    The original implementation in Django simply keeps the status code and
    does not allow developers to use custom HTTP status reason phrase, which
    is explicitly allowed by the HTTP specification:
    http://www.w3.org/Protocols/rfc2616/rfc2616-sec6.html
    
    """

    def __init__(self, content='', mimetype=None, status=None, *args, **kwargs):
        if isinstance(status, basestring):
            (status_code, status_reason) = status.split(' ', 1)
            status_code = int(status_code)
            self.status_reason = status_reason or None
        else:
            status_code = status
            self.status_reason = None
        super(TwodResponse, self).__init__(content, mimetype, status_code, *args, **kwargs)
        if self.status_reason:
            reason_header = '%s %s' % (self.status_code, self.status_reason)
            self._headers[_ACTUAL_REASON_HEADER.lower()] = (
             _ACTUAL_REASON_HEADER, reason_header)
        return


class DjangoApplication(WSGIHandler):
    """
    Django request handler which uses our enhanced WSGI request class.
    
    """
    request_class = TwodWSGIRequest

    def __call__(self, environ, start_response):
        start_response_wrapper = _StartResponseWrapper(start_response)
        return super(DjangoApplication, self).__call__(environ, start_response_wrapper)


class _StartResponseWrapper(object):
    """
    Wrapper for an actual start_response() callable which replaces the
    ``status`` with the actual status reason, if any.
    
    We need to iterate over all the ``response_headers`` until we find the
    actual status reason. If it's not there, we'd have wasted time and
    resources, but there's no other way around this until Django fixes the bug:
    http://code.djangoproject.com/ticket/12747
    
    """

    def __init__(self, original_start_response):
        self.original_start_response = original_start_response

    def __call__(self, status, response_headers, exc_info=None):
        final_headers = []
        for (header_name, header_value) in response_headers:
            if header_name == _ACTUAL_REASON_HEADER:
                status = header_value
            else:
                final_headers.append((header_name, header_value))

        return self.original_start_response(status, final_headers)