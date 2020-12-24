# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/guavacado/WebDispatcher.py
# Compiled at: 2020-04-06 13:25:25
# Size of source mod 2**32: 3243 bytes
from .version_number import guavacado_version
WebServerNameAndVer = 'Guavacado/' + guavacado_version
from .misc import init_logger, addr_rep
from .ConnListener import ConnListener
from .WebRequestHandler import WebRequestHandler
from datetime import datetime
import os, threading, fnmatch

class WebDispatcher(object):
    __doc__ = 'handles requests by identifying function based on the URL, then dispatching the request to the appropriate function'

    def __init__(self, addr=None, timeout=None, error_404_page_func=None, auth_handler=None):
        self.log_handler = init_logger(__name__)
        self.addr = addr
        self.timeout = timeout
        self.error_404_page_func = error_404_page_func
        self.resource_handlers = []
        self.auth_handler = auth_handler

    def handle_connection(self, clientsocket, address, client_id):
        handler = WebRequestHandler(clientsocket, address, client_id, (self.request_handler), timeout=(self.timeout), auth_handler=(self.auth_handler))
        handler.handle_connection()

    def get_resource_handler_index(self, name):
        for i in range(len(self.resource_handlers)):
            if self.resource_handlers[i]['name'] == name:
                return i

    def add_resource_handler(self, check_valid, handler_callback, name, level=None):
        """
                adds a resource handler to the list of resources to check when handling a request
                        check_valid should be a callable which returns a tuple of valid arguments for handler_callback if the resource is valid or None if the resource is invalid
                        handler_callback should be a callable which accepts the arguments returned by check_valid and handles the request, then returns the body of the message (in byte form) that should be returned
                        level should be None to take precedence over all previous handlers
                                or an index of a handler under which it should be placed in priority (returned by a previous call to add_resource_handler)
                                or the name of the handler under which it should be placed in priority
                """
        self.log_handler.debug('Adding resource handler "{name}" with valid checker {valid}() and handler {handler}()'.format(name=name, valid=(check_valid.__name__), handler=(handler_callback.__name__)))
        if level is None:
            level = len(self.resource_handlers)
        if isinstance(level, str):
            level = self.get_resource_handler_index(level)
        self.resource_handlers.insert(level, {'name':name, 
         'valid':check_valid, 
         'handler':handler_callback})
        return level

    def request_handler(self, url=None, method=None, headers=None, body=None):
        for handler in reversed(self.resource_handlers):
            valid = handler['valid'](url=url, method=method, headers=headers, body=body)
            if valid is not None:
                return (handler['handler'])(*valid)

    def get_address_string(self):
        return '{server} Server at {addr}'.format(server=WebServerNameAndVer, addr=addr_rep((self.addr), pretty=True))

    def get_404_page(self, request_handler_instance, url=''):
        if self.error_404_page_func is not None:
            return self.error_404_page_func(url=url)
        else:
            return '<html><head><title>404 Not Found</title></head><body><h1>Not Found</h1><p>The requested URL {url} was not found on this server.</p><hr><address>{address}</address></body></html>'.format(url=url, address=(self.get_address_string()))