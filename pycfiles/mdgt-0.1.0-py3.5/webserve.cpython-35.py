# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\mdgt\webserve.py
# Compiled at: 2016-10-17 15:09:43
# Size of source mod 2**32: 2292 bytes
"""webserve.py
mdgt web server module.
"""
from wsgiref import simple_server
from pathlib import Path
from .provider import Provider
import json

def mdgt_app(environ, start_response):
    """Entry point for the mdgt WSGI instance

    Args:
        environ (dict): Contains WSGI environment variables
        start_response (callable): A WSGI callable which sends status and
            headers before the request is processed in its entirety.
    """
    if environ['PATH_INFO'].startswith('/favicon'):
        status = '404 Not found'
        headers = [('Content-Type', "text/plain; charset='UTF-8'")]
        start_response(status, headers)
        return [
         'No favicon'.encode('utf-8')]
    else:
        args = environ['PATH_INFO'].split('/', 3)
        status = '200 OK'
        headers = [
         ('Content-Type', "application/json; charset='UTF-8'")]
        start_response(status, headers)
        if len(args) < 2:
            return JSON_error('Not enough parameters.')
        if args[1] == 'providers':
            return list_providers()
        if len(args) == 3:
            try:
                prov = Provider(args[1])
            except:
                return JSON_error('Provider does not exist. ' + args[1])

            return [json.dumps(prov.scrape(args[2])).encode('utf-8')]
        return JSON_error('Invalid arguments.')


def list_providers():
    """Outputs a list of providers."""
    p = Path('providers')
    provFiles = list(p.glob('*.json'))
    provs = [pf.stem for pf in provFiles]
    return [json.dumps(provs).encode('utf-8')]


def JSON_error(message):
    """Outputs a JSON error message.

    Args:
        message (str): A useful error message.
    """
    return [
     json.dumps({'error_message': message}).encode('utf-8')]


def serve(port=8181):
    """Starts a WSGI web server service.

    Args:
        port (Optional[int]): The port the server should listen at.  Defaults
            to 8181.
    """
    httpd = simple_server.make_server('', port, mdgt_app)
    try:
        print('Starting web server at http://localhost:{0!s}'.format(port))
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.socket.close()