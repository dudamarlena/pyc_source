# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/node_exporter/node_exporter.py
# Compiled at: 2020-01-14 05:18:01
# Size of source mod 2**32: 1957 bytes
from http.server import HTTPServer
import os
from sys import argv
from urllib.parse import quote_plus, parse_qs, urlparse
from prometheus_client import MetricsHandler, exposition
from collector.ccontroller import CController
__version__ = '0.3.5'

class NodeExporterServer(MetricsHandler):

    def do_GET(self):
        if urlparse(self.path).path != '/metrics':
            self.send_response(200)
            self.send_header('Content-Type', 'Content-Type: text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write('<html>\n            <head><title>Node Exporter</title></head>\n            <body>\n            <h1>Node Exporter</h1>\n            <p><a href="/metrics">Metrics</a></p>\n            </body>\n            </html>'.encode('utf-8'))
            return None
        params = parse_qs(urlparse(self.path).query)
        encoder, content_type = exposition.choose_encoder(self.headers.get('Accept'))
        if 'collect[]' in params:
            names = params['collect[]']
            CController.collect(names)
        try:
            output = encoder(self.registry)
        except:
            self.send_error(500, 'error generating metric output')
            raise
        else:
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.end_headers()
            self.wfile.write(output)


def run(server_class=HTTPServer, handler_class=NodeExporterServer, port=9100):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting node_exporter port{}...\n'.format(port))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    else:
        httpd.server_close()
        print('Stopping httpd...\n')


def main():
    if len(argv) == 2:
        run(port=(int(argv[1])))
    else:
        run()