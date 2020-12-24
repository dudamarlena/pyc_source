# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/producti_gestio/core/request_handler.py
# Compiled at: 2018-05-24 14:59:02
# Size of source mod 2**32: 7559 bytes
"""
producti_gestio.core.request_handler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
It handles the requests checking the
configuration, then pass all parameters
and headers to the **user-defined function**.

A **request handler** must have these requirements:

    * Have a ``do_GET`` function
    * Have a ``do_POST`` function

When a Server instance is started, the *request handler* will get the
configuration under ``self.configuration`` and the handlers under ``self.handlers``.
"""
import json, traceback, urllib.parse
from http.server import BaseHTTPRequestHandler
from typing import NewType
configuration = NewType('configuration', dict)
parameters = NewType('parameters', dict)

class RequestHandler(BaseHTTPRequestHandler):
    __doc__ = 'The RequestHandler class is used to\n    handle all requests, after they are\n    checked using the configuration.\n\n    It has got two needed methods: **do_GET** and **do_POST**,\n    they will be called by the HTTPServer classes, based on\n    the type of the request.\n\n    Actually, **HEAD** and **PUT** request methods are not\n    supported.\n    '
    configuration: configuration = {'allow_get':False, 
     'allow_post':True, 
     'function':lambda **kwargs: {'response_code':403, 
      'response':{'ok': False}}, 
     'debug':False, 
     'ip':'127.0.0.1', 
     'port':8000}
    handlers: list = []
    use_handler: bool = False

    def do_request(self, request_infos: dict) -> bool:
        """The ``do_request`` function is used to
        get a response from the *handler function* or
        from one of the *Handlers* and send it to the user.

        Args:
            request_infos (dict): A dictionary that will be passed to the Handler function or the Handler.

        Returns:
            bool: True if all went right, otherwise False.
        """
        response = None
        try:
            if not self.use_handler:
                response = (self.configuration['function'])(**request_infos)
                if not response:
                    raise BaseException('Got a ' + str(response) + ' <' + str(type(response)) + '>')
            else:
                for handler in self.handlers:
                    if handler.check(request_infos):
                        response = (handler.callback)(**request_infos)
                    else:
                        continue

                if not response:
                    raise BaseException('Got a ' + str(response) + ' <' + str(type(response)) + '>')
            self.send_response(response['response_code'])
            self.send_header('content-type', 'application/json')
            self.end_headers()
            self.wfile.write(bytes(json.dumps(response['response']), 'utf8'))
            return True
        except BaseException as e:
            if 'debug' in self.configuration:
                if self.configuration['debug']:
                    response = {'ok':False,  'traceback':str(traceback.format_exc())[:-1], 
                     'error':str(e)}
                    self.send_response(500)
                    self.send_header('content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(bytes(json.dumps(response), 'utf8'))
                    return False
            self.send_response(500)
            self.send_header('content-type', 'application/json')
            self.end_headers()
            self.wfile.write(bytes(json.dumps({'ok': False}), 'utf8'))
            return False

    def do_GET(self) -> bool:
        """The GET requests handler, it checks
        if GET is allowed as method and then
        parse the request and pass it to a
        defined function and return a response.

        Returns:
          bool: True if the request succeeded, False if not or GET is not allowed.

        """
        if 'allow_get' in self.configuration:
            if self.configuration['allow_get']:
                self.do_request({'parameters':urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query), 
                 'request-type':self.command, 
                 'path':self.path, 
                 'header':self.headers, 
                 'object':self})
        else:
            self.send_response(405)
            return False

    def parse_post(self) -> parameters:
        """The POST parameters parser. It checks the
        self.headers dictionary, its content-type and
        if it is 'multipart/form-data' or 'application/x-www-form-urlencoded', then
        parses the POST parameters.

        Returns:
          dict: POST parameters in a dictionary, where the keys are the parameter names and the values are their values.

        """
        postvars = {}
        try:
            try:
                length = int(self.headers['content-length'])
                postvars = urllib.parse.parse_qs((self.rfile.read(length)),
                  keep_blank_values=1)
            except:
                postvars = {}

        finally:
            return

        return postvars

    def do_POST(self) -> bool:
        """The POST requests handler, it checks
        if POST is allowed as method and then
        parse the request and pass it to a
        defined function and return a response.

        Returns:
          bool: True if the request succeeeded, False if not or POST is not allowed.

        """
        if 'allow_post' in self.configuration:
            if self.configuration['allow_post']:
                self.do_request({'parameters':self.parse_post(),  'request-type':self.command, 
                 'path':self.path, 
                 'header':self.headers, 
                 'object':self})
        else:
            self.send_response(405)
            return False