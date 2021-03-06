# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/wymypy/libs/wsgiserver.py
# Compiled at: 2007-01-13 08:09:10
""" wsgiServer

                Copyright (c) 2004 Colin Stewart (http://www.owlfish.com/)
                All rights reserved.

                Redistribution and use in source and binary forms, with or without
                modification, are permitted provided that the following conditions
                are met:
                1. Redistributions of source code must retain the above copyright
                   notice, this list of conditions and the following disclaimer.
                2. Redistributions in binary form must reproduce the above copyright
                   notice, this list of conditions and the following disclaimer in the
                   documentation and/or other materials provided with the distribution.
                3. The name of the author may not be used to endorse or promote products
                   derived from this software without specific prior written permission.

                THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
                IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
                OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
                IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
                INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
                NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
                DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
                THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
                (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
                THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

                If you make any bug fixes or feature enhancements please let me know!

                A basic multi-threaded WSGI server.
"""
import SimpleHTTPServer, SocketServer, BaseHTTPServer, urlparse, sys, logging, socket, errno, traceback, StringIO
SERVER_ERROR = '<html>\n  <head>\n    <title>Server Error</title>\n  </head>\n  <body>\n    <h1>Server Error</h1>\n    A server error has occurred.  Please contact the system administrator for\n    more information.\n  </body>\n</html>\n'

class WSGIHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    __module__ = __name__

    def log_message(self, *args):
        pass

    def log_request(self, *args):
        pass

    def getApp(self):
        (protocol, host, path, parameters, query, fragment) = urlparse.urlparse('http://dummyhost%s' % self.path)
        for (appPath, app) in self.server.wsgiApplications:
            if path.startswith(appPath):
                pathInfo = path[len(appPath):]
                if len(pathInfo) > 0:
                    if not pathInfo.startswith('/'):
                        pathInfo = '/' + pathInfo
                if appPath.endswith('/'):
                    scriptName = appPath[:-1]
                else:
                    scriptName = appPath
                return (app, scriptName, pathInfo, query)

        return (None, None, None, None)

    def do_GET(self):
        (app, scriptName, pathInfo, query) = self.getApp()
        if not app:
            if self.server.serveFiles:
                SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
                return
            self.send_error(404, 'Application not found.')
            return
        self.runWSGIApp(app, scriptName, pathInfo, query)

    def do_POST(self):
        (app, scriptName, pathInfo, query) = self.getApp()
        if not app:
            self.send_error(404, 'Application not found.')
            return
        self.runWSGIApp(app, scriptName, pathInfo, query)

    def runWSGIApp(self, application, scriptName, pathInfo, query):
        logging.info('Running application with script name %s path %s' % (scriptName, pathInfo))
        env = {'wsgi.version': (1, 0), 'wsgi.url_scheme': 'http', 'wsgi.input': self.rfile, 'wsgi.errors': sys.stderr, 'wsgi.multithread': 1, 'wsgi.multiprocess': 0, 'wsgi.run_once': 0, 'REQUEST_METHOD': self.command, 'SCRIPT_NAME': scriptName, 'PATH_INFO': pathInfo, 'QUERY_STRING': query, 'CONTENT_TYPE': self.headers.get('Content-Type', ''), 'CONTENT_LENGTH': self.headers.get('Content-Length', ''), 'REMOTE_ADDR': self.client_address[0], 'SERVER_NAME': self.server.server_address[0], 'SERVER_PORT': str(self.server.server_address[1]), 'SERVER_PROTOCOL': self.request_version}
        for (httpHeader, httpValue) in self.headers.items():
            env['HTTP_%s' % httpHeader.replace('-', '_').upper()] = httpValue

        self.wsgiSentHeaders = 0
        self.wsgiHeaders = []
        try:
            result = application(env, self.wsgiStartResponse)
            try:
                try:
                    for data in result:
                        if data:
                            self.wsgiWriteData(data)

                finally:
                    if hasattr(result, 'close'):
                        result.close()
            except socket.error, socketErr:
                if socketErr.args[0] in (errno.ECONNABORTED, errno.EPIPE):
                    logging.debug('Network error caught: (%s) %s' % (str(socketErr.args[0]), socketErr.args[1]))
                    return
            except socket.timeout, socketTimeout:
                logging.debug('Socket timeout')
                return

        except:
            errorMsg = StringIO.StringIO()
            traceback.print_exc(file=errorMsg)
            logging.error(errorMsg.getvalue())
            if not self.wsgiSentHeaders:
                self.wsgiStartResponse('500 Server Error', [('Content-type', 'text/html')])
            self.wsgiWriteData(SERVER_ERROR)

        if not self.wsgiSentHeaders:
            self.wsgiWriteData(' ')

    def wsgiStartResponse(self, response_status, response_headers, exc_info=None):
        if self.wsgiSentHeaders:
            raise Exception('Headers already sent and start_response called again!')
        self.wsgiHeaders = (response_status, response_headers)
        return self.wsgiWriteData

    def wsgiWriteData(self, data):
        if not self.wsgiSentHeaders:
            (status, headers) = self.wsgiHeaders
            statusCode = status[:status.find(' ')]
            statusMsg = status[status.find(' ') + 1:]
            self.send_response(int(statusCode), statusMsg)
            for (header, value) in headers:
                self.send_header(header, value)

            self.end_headers()
            self.wsgiSentHeaders = 1
        self.wfile.write(data)


class WSGIServer(SocketServer.ThreadingMixIn, BaseHTTPServer.HTTPServer):
    __module__ = __name__

    def __init__(self, serverAddress, wsgiApplications, serveFiles=1):
        BaseHTTPServer.HTTPServer.__init__(self, serverAddress, WSGIHandler)
        appList = []
        for (urlPath, wsgiApp) in wsgiApplications.items():
            appList.append((urlPath, wsgiApp))

        self.wsgiApplications = appList
        self.serveFiles = serveFiles
        self.serverShuttingDown = 0