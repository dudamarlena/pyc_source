# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nb/publish/btw/tingyun/tingyun/armoury/framework_tornado.py
# Compiled at: 2016-06-30 06:13:10
"""
"""
import logging
from tingyun.armoury.ammunition.external_tracker import wrap_external_trace
from tingyun.armoury.ammunition.tornado_tracker.httpserver import connection_on_headers_wrapper
from tingyun.armoury.ammunition.tornado_tracker.httpserver import connect_on_request_body_wrapper
from tingyun.armoury.ammunition.tornado_tracker.httpserver import connection_finish_request_wrapper
from tingyun.armoury.ammunition.tornado_tracker.httpserver import iostream_close_callback_wrapper
from tingyun.armoury.ammunition.tornado_tracker.web import trace_request_exception, trace_wsgi_app_entrance
from tingyun.armoury.ammunition.tornado_tracker.web import trace_request_execute, trace_request_init
console = logging.getLogger(__name__)

def detect_wsgi_server_entrance(module):
    """
    :param module:
    :return:
    """
    pass


def detect_wsgi_app_entrance(module):
    """
    """
    module.Application.__call__ = trace_wsgi_app_entrance(module.Application.__call__)
    if hasattr(module, 'RequestHandler'):
        module.RequestHandler.__init__ = trace_request_init(module.RequestHandler.__init__)
        module.RequestHandler._handle_request_exception = trace_request_exception(module.RequestHandler._handle_request_exception)
        module.RequestHandler._execute = trace_request_execute(module.RequestHandler._execute)


def detect_tornado_main_process(module):
    """all of the data handled in HTTPConnection class, include build header/body/finish
    :param module:
    :return:
    """
    if hasattr(module, 'HTTPConnection'):
        module.HTTPConnection._on_headers = connection_on_headers_wrapper(module.HTTPConnection._on_headers)
        module.HTTPConnection._on_request_body = connect_on_request_body_wrapper(module.HTTPConnection._on_request_body)
        module.HTTPConnection._finish_request = connection_finish_request_wrapper(module.HTTPConnection._finish_request)


def detect_iostream(module):
    """
    :param module:
    :return:
    """
    if hasattr(module, 'BaseIOStream'):
        module.BaseIOStream._maybe_run_close_callback = iostream_close_callback_wrapper(module.BaseIOStream._maybe_run_close_callback)


def detect_simple_httpclient(module):
    """
    :param module:
    :return:
    """

    def parse_url(instance, request, *args, **kwargs):
        return request

    wrap_external_trace(module, 'SimpleAsyncHTTPClient.fetch', 'simple_httpclient', parse_url)


def detect_curl_httpclient(module):
    """
    :param module:
    :return:
    """

    def parse_url(instance, request, *args, **kwargs):
        return request

    wrap_external_trace(module, 'CurlAsyncHTTPClient.fetch', 'curl_httpclient', parse_url)