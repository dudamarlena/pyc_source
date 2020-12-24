# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/porthole/server.py
# Compiled at: 2020-03-19 22:07:58
# Size of source mod 2**32: 4278 bytes
import sys, os, datetime, json, mimetypes
if sys.version_info.major < 3:
    from urlparse import urlparse, parse_qs
    import SocketServer
    from SimpleHTTPServer import SimpleHTTPRequestHandler
else:
    from urllib.parse import urlparse, parse_qs
    from http.server import SimpleHTTPRequestHandler, socketserver as SocketServer
ResoursePath = os.path.dirname(__file__) + '/static'
RequestHandlers = {}

def df(opts=''):
    outputLines = os.popen('df ' + opts).read().splitlines()
    keywords = outputLines[0].split()
    disks = []
    for i in range(1, len(outputLines)):
        disk = {}
        values = outputLines[i].split()
        for j in range(len(values)):
            disk[keywords[j]] = values[j]

        disks.append(disk)

    return disks


def vmstat(opts=''):
    outputLines = os.popen('vmstat ' + opts).read().splitlines()
    keywords = outputLines[(-2)].split()
    cpu = {}
    values = outputLines[(-1)].split()
    for i in range(len(values)):
        cpu[keywords[i]] = values[i]

    return cpu


RequestHandlers.update({'/df': df})
RequestHandlers.update({'/vmstat': vmstat})

def onGet(path, handler):
    RequestHandlers.update({path: handler})


class PortHoleHandler(SimpleHTTPRequestHandler):

    def serve(self):
        global ResoursePath
        tmp = self.path.split('?', 1)
        path = tmp[0]
        qs = tmp[1] if len(tmp) > 1 else ''
        queryParam = parse_qs(qs)
        if path in RequestHandlers:
            data = RequestHandlers.get(path)()
            contentType = 'application/json'
            if data is str:
                try:
                    json.loads(data)
                except:
                    contentType = 'text/plain'

            else:
                data = json.dumps(data)
            self.response['code'] = 200
            self.response['contentType'] = contentType
            self.response['data'] = data
            return
        if path == '/' or path == '':
            path = '/index.html'
        self.response['code'] = 200
        self.response['contentType'] = self.guess_type(path)
        self.response['filePath'] = os.path.abspath(ResoursePath) + path

    def onError(self, error):
        self.response['code'] = 500
        self.response['contentType'] = 'text/plain'
        self.response['data'] = str(error)

    def do_GET(self):
        self.response = {'code': 200, 'contentType': '', 'data': None, 'filePath': None}
        try:
            try:
                self.serve()
            except Exception as error:
                self.onError(error)

        finally:
            if self.response['filePath'] != None:
                try:
                    f = open(self.response['filePath'], 'rb')
                    fs = os.fstat(f.fileno())
                    self.send_response(200)
                    self.send_header('Content-type', self.guess_type(self.response['filePath']))
                    self.send_header('Content-Length', str(fs[6]))
                    self.send_header('Last-Modified', self.date_time_string(fs.st_mtime))
                    self.end_headers()
                    self.copyfile(f, self.wfile)
                    f.close()
                    return
                except Exception as fErr:
                    self.send_response(404, 'file not found : ' + self.response['filePath'])
                    return

            self.send_response(200)
            self.send_header('Content-type', self.response['contentType'])
            self.send_header('Content-Length', len(self.response['data']))
            self.end_headers()
            self.wfile.write(self.response['data'].encode())


def serve(host='', port=8000):
    print('Porthole server at :[' + host + ':' + str(port) + ']')
    httpd = SocketServer.TCPServer((host, port), PortHoleHandler)
    httpd.serve_forever()