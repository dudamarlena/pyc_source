# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/guavacado/RedirectDispatcher.py
# Compiled at: 2019-06-26 12:47:28
# Size of source mod 2**32: 1193 bytes
from .version_number import guavacado_version
WebServerNameAndVer = 'Guavacado/' + guavacado_version
from .misc import generate_redirect_page_w_statuscode, init_logger
from .ConnListener import ConnListener
from .WebRequestHandler import WebRequestHandler
from datetime import datetime
import os, threading, fnmatch

class RedirectDispatcher(object):
    __doc__ = 'handles requests by identifying function based on the URL, then dispatching the request to the appropriate function'

    def __init__(self, timeout=None, target_domain='https://localhost/'):
        self.log_handler = init_logger(__name__)
        self.timeout = timeout
        self.target_domain = target_domain

    def handle_connection(self, clientsocket, address, client_id):
        handler = WebRequestHandler(clientsocket, address, client_id, (self.request_handler), timeout=(self.timeout))
        handler.handle_connection()

    def request_handler(self, url=None, method=None, headers=None, body=None):
        if url[0] == '/':
            rel_url = url[1:]
        else:
            rel_url = url
        if self.target_domain[(-1)] == '/':
            sep = ''
        else:
            sep = '/'
        dest = self.target_domain + sep + rel_url
        return generate_redirect_page_w_statuscode(dest)