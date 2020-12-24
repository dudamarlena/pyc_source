# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/compliance_suite/report_server.py
# Compiled at: 2018-09-24 11:22:10
# Size of source mod 2**32: 932 bytes
import http.server, socketserver, os, socket, webbrowser, sys
WEB_DIR = os.path.join(os.path.dirname(__file__), 'web')

def get_free_port():
    """ get_free_port function is used in conftest and the return of this
    is a free port available in the system on which the mock server will be
    run. This port will be passed to start_mock_server as a required parameter
    from conftest.py
    """
    s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    address, port = s.getsockname()
    s.close()
    return port


def start_mock_server(port=7878):
    os.chdir(WEB_DIR)
    port = get_free_port()
    Handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(('', port), Handler)
    print('serving at http://localhost:' + str(port), file=sys.stderr)
    webbrowser.open('http://localhost:' + str(port))
    httpd.serve_forever()