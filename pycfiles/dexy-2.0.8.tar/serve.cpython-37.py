# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ana/dev/dexy-clean/dexy/commands/serve.py
# Compiled at: 2020-03-18 15:12:33
# Size of source mod 2**32: 5453 bytes
from dexy.commands.utils import init_wrapper
from dexy.utils import file_exists
import dexy.load_plugins, dexy.reporter, http.server, os, socket, socketserver, sys
NO_OUTPUT_MSG = "Please run dexy first, or specify a directory to serve. For help run 'dexy help -on serve'"

class SimpleHTTPAuthRequestHandler(http.server.SimpleHTTPRequestHandler):

    def send_head(self):
        """Common code for GET and HEAD commands.

        This sends the response code and MIME headers.

        Return value is either a file object (which has to be copied
        to the outputfile by the caller unless the command was HEAD,
        and must be closed by the caller under all circumstances), or
        None, in which case the caller has nothing further to do.

        """
        if self.headers.getheader('Authorization') == None:
            self.send_response(401)
            self.send_header('WWW-Authenticate', 'Basic realm="%s"' % self.__class__.realm)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write('no authorization received')
        else:
            if self.headers.getheader('Authorization') != 'Basic %s' % self.__class__.authcode:
                self.send_response(401)
                self.send_header('WWW-Authenticate', 'Basic realm="%s"' % self.__class__.realm)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write('not authenticated')
            else:
                path = self.translate_path(self.path)
                f = None
                if os.path.isdir(path):
                    if not self.path.endswith('/'):
                        self.send_response(301)
                        self.send_header('Location', self.path + '/')
                        self.end_headers()
                        return
                    for index in ('index.html', 'index.htm'):
                        index = os.path.join(path, index)
                        if os.path.exists(index):
                            path = index
                            break
                    else:
                        return self.list_directory(path)

                ctype = self.guess_type(path)
        try:
            f = open(path, 'rb')
        except IOError:
            self.send_error(404, 'File not found')
            return
        else:
            self.send_response(200)
            self.send_header('Content-type', ctype)
            fs = os.fstat(f.fileno())
            self.send_header('Content-Length', str(fs[6]))
            self.send_header('Last-Modified', self.date_time_string(fs.st_mtime))
            self.end_headers()
            return f


def serve_command(port=-1, reporters=[
 'ws', 'output'], username='', password='', realm='Dexy', directory=False, **kwargs):
    """
    Runs a simple web server on dexy-generated files.
    
    Will look first to see if the Website Reporter has run, if so this content
    is served. If not the standard output/ directory contents are served. You
    can also specify another directory to be served. The port defaults to 8085,
    this can also be customized. If a username and password are provided, uses
    HTTP auth to access pages.
    """
    if not directory:
        wrapper = init_wrapper(locals(), True)
        for alias in reporters:
            report_dir = dexy.reporter.Reporter.create_instance(alias).setting('dir')
            print('report dir', report_dir)
            if report_dir and file_exists(report_dir):
                directory = report_dir
                break

    else:
        if not directory:
            print(NO_OUTPUT_MSG)
            sys.exit(1)
        else:
            os.chdir(directory)
            if port < 0:
                ports = range(8085, 8100)
            else:
                ports = [
                 port]
        p = None
        for p in ports:
            try:
                if username and password:
                    import base64
                    authcode = base64.b64encode('%s:%s' % (username, password))
                    Handler = SimpleHTTPAuthRequestHandler
                    Handler.authcode = authcode
                    Handler.realm = realm
                else:
                    Handler = http.server.SimpleHTTPRequestHandler
                httpd = socketserver.TCPServer(('', p), Handler)
            except socket.error:
                print('port %s already in use' % p)
                p = None
            else:
                break

        if p:
            print('serving contents of %s on http://localhost:%s' % (directory, p))
            if username:
                if password:
                    if Handler.authcode:
                        print("username '%s' and password '%s' are required to access contents" % (username, password))
            print('type ctrl+c to stop')
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                sys.exit(1)

        else:
            print('could not find a free port to serve on, tried', ports)
            sys.exit(1)