# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/pyhttps.py
# Compiled at: 2017-09-05 08:04:46
import argparse, atexit, logging, os, sys, tempfile
from subprocess import call
from version import version
logging.basicConfig(level=logging.INFO)
PY3 = sys.version_info[0] == 3
parser = argparse.ArgumentParser(description='')
parser.add_argument('--host', dest='host', default='localhost')
parser.add_argument('--port', dest='port', type=int, default=4443)
args = parser.parse_args()
server_host = args.host
server_port = args.port
ssl_cert_path = ('{}/server.pem').format(tempfile.gettempdir())
if PY3:
    OpenSslExecutableNotFoundError = FileNotFoundError
else:
    OpenSslExecutableNotFoundError = OSError

def create_ssl_cert():
    if PY3:
        from subprocess import DEVNULL
    else:
        DEVNULL = open(os.devnull, 'wb')
    try:
        ssl_exec_list = [
         'openssl', 'req', '-new', '-x509', '-keyout', ssl_cert_path,
         '-out', ssl_cert_path, '-days', '365', '-nodes',
         '-subj', '/CN=www.talhasch.com/O=Talhasch Inc./C=TR']
        call(ssl_exec_list, stdout=DEVNULL, stderr=DEVNULL)
    except OpenSslExecutableNotFoundError:
        logging.error('openssl executable not found!')
        exit(1)

    logging.info(('Self signed ssl certificate created at {}').format(ssl_cert_path))


def exit_handler():
    os.remove(ssl_cert_path)
    logging.info('Bye!')


def main():
    logging.info(('pyhttps {}').format(version))
    create_ssl_cert()
    atexit.register(exit_handler)
    if PY3:
        import http.server, socketserver, ssl
        logging.info(('Server running... https://{}:{}').format(server_host, server_port))
        httpd = socketserver.TCPServer((server_host, server_port), http.server.SimpleHTTPRequestHandler)
        httpd.socket = ssl.wrap_socket(httpd.socket, certfile=ssl_cert_path, server_side=True)
    else:
        import BaseHTTPServer, SimpleHTTPServer, ssl
        logging.info(('Server running... https://{}:{}').format(server_host, server_port))
        httpd = BaseHTTPServer.HTTPServer((server_host, server_port), SimpleHTTPServer.SimpleHTTPRequestHandler)
        httpd.socket = ssl.wrap_socket(httpd.socket, certfile=ssl_cert_path, server_side=True)
    httpd.serve_forever()