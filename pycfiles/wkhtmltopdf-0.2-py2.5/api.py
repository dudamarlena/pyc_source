# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/wkhtmltopdf/api.py
# Compiled at: 2011-07-21 06:58:59
import optparse, os, random, time, urlparse
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from main import WKhtmlToPdf
HOST = '127.0.0.1'
PORT = 8888

def run_server(handler, host, port):
    server = HTTPServer((host, port), handler)
    try:
        server.serve_forever()
        print time.asctime(), 'Starting server (http://%s:%s), use <Ctrl-C> to stop' % (host, port)
        return True
    except KeyboardInterrupt:
        server.server_close()
        print time.asctime(), 'Stopping server (http://%s:%s)' % (host, port)
        return True


class RequestHandler(BaseHTTPRequestHandler):
    """
    Simple request class to serve json response back to ajax application.
    """

    def handle_headers(self, status_code):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', host)
        self.end_headers()

    def handle_404(self, message):
        self.handle_headers(404)
        self.wfile.write('{"error": "%s"}"' % message)
        self.end_headers()

    def handle_500(self, message):
        self.handle_headers(500)
        self.wfile.write('{"error": "%s"}"' % message)

    def handle_200(self, message, file_path=None):
        self.send_response(200)
        if file_path:
            self.send_header('Content-Type', 'application/pdf')
            self.end_headers()
            self.wfile.write(open(file_path, 'r').read())
        else:
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write('{"success": "%s"}"' % message)

    def do_GET(self):
        self.urlparser = urlparse.urlparse(self.path)
        self.query_string = self.urlparser.query
        self.query_dict = urlparse.parse_qs(self.query_string)
        self.url = self.query_dict.get('url', [None])[0]
        self.output_file = self.query_dict.get('output_file', [None])[0]
        if not self.url or not self.output_file:
            self.handle_404('url and output_file params are required')
            return
        options_dict = {}
        for (k, v) in self.query_dict.items():
            options_dict[k] = v[0]

        wkhtp = WKhtmlToPdf(self.url, self.output_file, **options_dict)
        output_file = wkhtp.render()
        if output_file[0]:
            self.handle_200('the file has been saved', output_file[1])
        else:
            self.handle_500('%s - the file could not be created' % output_file[1])
        return


if __name__ == '__main__':
    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser()
    parser.add_option('-H', '--host', dest='host', default=HOST, help='server host name')
    parser.add_option('-p', '--port', dest='port', default=PORT, help='port to run the api on')
    (options, args) = parser.parse_args()
    host = options.host
    port = int(options.port)
    run_server(RequestHandler, host, port)