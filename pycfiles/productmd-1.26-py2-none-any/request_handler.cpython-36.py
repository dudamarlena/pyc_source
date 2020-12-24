# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/producti_gestio/core/request_handler.py
# Compiled at: 2018-05-24 14:59:02
# Size of source mod 2**32: 7559 bytes
__doc__ = '\nproducti_gestio.core.request_handler\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nIt handles the requests checking the\nconfiguration, then pass all parameters\nand headers to the **user-defined function**.\n\nA **request handler** must have these requirements:\n\n    * Have a ``do_GET`` function\n    * Have a ``do_POST`` function\n\nWhen a Server instance is started, the *request handler* will get the\nconfiguration under ``self.configuration`` and the handlers under ``self.handlers``.\n'
import json, traceback, urllib.parse
from http.server import BaseHTTPRequestHandler
from typing import NewType
configuration = NewType('configuration', dict)
parameters = NewType('parameters', dict)

class RequestHandler(BaseHTTPRequestHandler):
    """RequestHandler"""
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