# uncompyle6 version 3.6.7
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ploader/tests/environment_handler.py
# Compiled at: 2014-01-14 07:49:27
# Size of source mod 2**32: 777 bytes
import http.server, threading, socketserver, os
from ploader.utils import set_config_path

def create_http_server(port):
    httpd = socketserver.TCPServer(('0.0.0.0', port), http.server.SimpleHTTPRequestHandler)
    thread = threading.Thread(target=httpd.serve_forever)
    thread.start()
    return httpd


def handle_cwd(path='ploader/tests/cwd'):
    try:
        os.chdir(path)
    except FileNotFoundError:
        pass

    set_config_path('../../../config.yaml')


def create_test_config(path='./config.yaml'):
    basic_conf = 'download-dir: somewhere\ncaptcha-api-key: foo\nport: 42424'
    with open(path, 'w') as (fd):
        fd.write(basic_conf)