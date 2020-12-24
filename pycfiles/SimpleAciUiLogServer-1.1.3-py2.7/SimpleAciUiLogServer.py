# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/SimpleAciUiLogServer/SimpleAciUiLogServer.py
# Compiled at: 2015-08-16 18:06:32
"""A Simple HTTP server that acts as a remote API Inspector for the APIC GUI.

Written by Mike Timm (mtimm@cisco.com)
Based on code written by Fredrik Lundh & Brian Quinlan.
"""
from argparse import ArgumentParser
import BaseHTTPServer, cgi, json, logging, os, re, select, signal, SocketServer, socket, ssl
from StringIO import StringIO
import sys, tempfile
try:
    import fcntl
except ImportError:
    fcntl = None

SERVER_CERT = '\n-----BEGIN RSA PRIVATE KEY-----\nMIICXAIBAAKBgQC+oA+hYsF3uBIMt7i1ELfUFnyf4/MKM/Ylmy4yBc0/YhqANXYk\nso3+gAGkgRlv9ODdsFS7KvjzyaT0kjgA3ahDPyvtroAOWsdFdHJvtS4Ek1WI1Bee\n0hNZlTmjQgnjp9ENYl9ImGWghcubJhtse5cJhL9c/hq40do4llZjaaEiCQIDAQAB\nAoGAYbd1K7qPCErAXeqT8aVXRo4cZm4YeSN3y4FH5faZZyNoCE7feCJbrZl6vhQ7\nsOtrldi9JpD5uyaju4d00+TMSoFqnTuAYLg4CEUAkAq2Hgg1EfQfPpC8IgYdR5qQ\nhRu0JArXldch1YLHw8GQGkkZe/cJXiHs/FPjmdUQSsydI50CQQDuEecLrSLjuMpE\ni8xjD9cQxSDTHJFDZttVb08fjaKFJk993TsUR2t/eR92OR5m0CFei/RUyYpUaPbk\n1s3Eau7XAkEAzPtnMMKoGR3qfLqXzfmgLwQA0UbeV8PbxRCkaCnSYcpn0qJH7UtS\nQjb4X6MPA9bNUnydWFgbPgz4MwKRo0q6HwJAP6DxS6GerZZ6GQ/0NJXLOWQ2fbYo\n7QbUoGT7lMdaJJQ0ssMqQyVDifJpgkOJ6JjAEnD9gJvNKPpU4py2qkSaSQJANngr\n0Jo5XwtDD0fqJPLLbRLsQLBLTxkdoj0s4v0SCahmdGNpJ5ZXUn8W+xryV3vR7bRt\nf1dSTefWYH+zQagO0wJBANlNp79CN7ylgXdrhRVQmBsXHN4G8biUUxMYsfK4Ao/i\nGa3xtkYLv7OmrtY+Gx6w56Jqxyucaka8VBHK0/7JTLE=\n-----END RSA PRIVATE KEY-----\n-----BEGIN CERTIFICATE-----\nMIID+jCCA2OgAwIBAgIJALUh5RwHQhJoMA0GCSqGSIb3DQEBBQUAMIGvMQswCQYD\nVQQGEwJVUzELMAkGA1UECBMCQ0ExETAPBgNVBAcTCFNhbiBKb3NlMRUwEwYDVQQK\nEwxhcGlpbnNwZWN0b3IxHTAbBgNVBAsTFFNpbXBsZUFjaVVpTG9nU2VydmVyMSow\nKAYDVQQDEyFTaW1wbGVBY2lVaUxvZ1NlcnZlci5hcGlpbnNwZWN0b3IxHjAcBgkq\nhkiG9w0BCQEWD210aW1tQGNpc2NvLmNvbTAgFw0xNTAxMjMwMDI1NDJaGA8zMDE0\nMDUyNjAwMjU0Mlowga8xCzAJBgNVBAYTAlVTMQswCQYDVQQIEwJDQTERMA8GA1UE\nBxMIU2FuIEpvc2UxFTATBgNVBAoTDGFwaWluc3BlY3RvcjEdMBsGA1UECxMUU2lt\ncGxlQWNpVWlMb2dTZXJ2ZXIxKjAoBgNVBAMTIVNpbXBsZUFjaVVpTG9nU2VydmVy\nLmFwaWluc3BlY3RvcjEeMBwGCSqGSIb3DQEJARYPbXRpbW1AY2lzY28uY29tMIGf\nMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC+oA+hYsF3uBIMt7i1ELfUFnyf4/MK\nM/Ylmy4yBc0/YhqANXYkso3+gAGkgRlv9ODdsFS7KvjzyaT0kjgA3ahDPyvtroAO\nWsdFdHJvtS4Ek1WI1Bee0hNZlTmjQgnjp9ENYl9ImGWghcubJhtse5cJhL9c/hq4\n0do4llZjaaEiCQIDAQABo4IBGDCCARQwHQYDVR0OBBYEFN2EqumA49KSEPjLLSni\nUtKth4zQMIHkBgNVHSMEgdwwgdmAFN2EqumA49KSEPjLLSniUtKth4zQoYG1pIGy\nMIGvMQswCQYDVQQGEwJVUzELMAkGA1UECBMCQ0ExETAPBgNVBAcTCFNhbiBKb3Nl\nMRUwEwYDVQQKEwxhcGlpbnNwZWN0b3IxHTAbBgNVBAsTFFNpbXBsZUFjaVVpTG9n\nU2VydmVyMSowKAYDVQQDEyFTaW1wbGVBY2lVaUxvZ1NlcnZlci5hcGlpbnNwZWN0\nb3IxHjAcBgkqhkiG9w0BCQEWD210aW1tQGNpc2NvLmNvbYIJALUh5RwHQhJoMAwG\nA1UdEwQFMAMBAf8wDQYJKoZIhvcNAQEFBQADgYEABPx5cxBNOjWOxZbiRVfpzKac\nMKs4tFNtEmilAY7kvNouGaSl1Yw2fCpGXjstOG0+SxPy34YgeQSVOGQI1KXhd7vk\nnALqxrKiP2rzpZveBkjq5voRpFw2creEXyt76EKQgwRHYJP60Vu3bYnYNoFHdUwE\nTOBaHjC6ZZLRd77dd3s=\n-----END CERTIFICATE-----\n'

class SimpleLogDispatcher(object):
    """A class to dispatch log messages."""
    loglevel = {'DEBUG': logging.DEBUG, 
       'INFO': logging.INFO, 
       'WARN': logging.WARNING, 
       'ERROR': logging.ERROR, 
       'FATAL': logging.CRITICAL}
    indent = 4
    prettyprint = False
    strip_imdata = False

    def __init__(self, allow_none=False, excludes=None, request_types=None):
        """Initialize a SimpleLogDispatcher instance."""
        self.funcs = {}
        self.instance = None
        self.allow_none = allow_none
        if excludes is None:
            self.excludes = []
        else:
            self.excludes = excludes
        if request_types is None:
            self.request_types = [
             'all']
        else:
            self.request_types = request_types
        return

    def register_instance(self, instance):
        """Register an instance of a class to dispatch to."""
        self.instance = instance

    def register_function(self, function, name=None):
        """Register a function to respond to Log requests.

        The optional name argument can be used to set a Unicode name
        for the function.
        """
        if name is None:
            name = function.__name__
        self.funcs[name] = function
        return

    def dispatch(self, method, params):
        """Dispatch log messages."""
        method = method.replace(' ', '')
        if 'all' not in self.request_types and method not in self.request_types:
            return
        self._dispatch(method, params)

    def _dispatch(self, method, params):
        """Internal dispatch method."""
        func = None
        try:
            func = self.funcs[method]
        except KeyError:
            if self.instance is not None:
                if hasattr(self.instance, '_dispatch'):
                    return self.instance.dispatch(method, params)
                func = method

        if func is not None:
            if 'data' in params.keys() and self._excludes(self._get_method(**params), self._get_url(method, **params)):
                return ''
            return func(**params)
        else:
            datastring = ''
            paramkeys = params.keys()
            if 'data' not in paramkeys:
                level = logging.DEBUG
                datastring = 'No data found'
            else:
                level = self._get_loglevel(**params)
                method = self._get_method(**params)
                url = self._get_url(method, **params)
                payload = self._get_payload(method, **params)
                response, response_dict = self._get_response(**params)
                total_count = self._get_total_count(response_dict)
                if self._excludes(method, url):
                    return ''
                datastring += ('    method: {0}\n').format(method)
                datastring += ('       url: {0}\n').format(url)
                datastring += ('   payload: {0}\n').format(payload)
                datastring += ('    # objs: {0}\n').format(total_count)
                datastring += ('  response: {0}\n').format(self._strip_imdata(response_dict))
            logging.log(level, datastring)
            return datastring
            return

    def _excludes(self, method, url):
        """Internal method to exclude certain types of log messages."""
        if method != 'GET':
            return False
        for excl in self.excludes:
            if excl == 'topInfo' and 'info.json' in url:
                return True
            if str(excl) + '.json' in url:
                return True

        return False

    @staticmethod
    def _get_total_count(response_dict):
        """Extract object count if any."""
        try:
            return response_dict['total_count']
        except KeyError:
            return '0'

    @staticmethod
    def _get_response(**params):
        """Extract the respone if any."""
        try:
            response = params['data']['response']
            response_dict = json.loads(response)
        except KeyError:
            response = 'None'
            response_dict = {}

        return (
         response, response_dict)

    def _get_payload(self, method, **params):
        """Extract the payload if any."""
        try:
            payload = params['data']['payload']
            if self.prettyprint:
                payload = '\n' + json.dumps(json.loads(payload), indent=self.indent)
        except KeyError:
            payload = 'N/A' if method == 'Event Channel Message' else 'None'

        return payload

    @staticmethod
    def _get_url(method, **params):
        """Extract the URL."""
        try:
            url = params['data']['url']
        except KeyError:
            url = 'N/A' if method == 'Event Channel Message' else 'None'

        return url

    @staticmethod
    def _get_method(**params):
        """Extract the HTTP method (verb)."""
        try:
            return params['data']['method']
        except KeyError:
            return

        return

    def _get_loglevel(self, **params):
        """Exract the loglevel if any."""
        try:
            preamble = params['data']['preamble']
            return self.loglevel[preamble.split(' ')[1]]
        except KeyError:
            return logging.DEBUG

    def _strip_imdata(self, json_dict):
        """Strip out the imdata."""
        if 'imdata' not in json_dict.keys():
            return 'None'
        else:
            if self.strip_imdata:
                return self._pretty_print(json_dict['imdata'])
            return self._pretty_print(json_dict)

    def _pretty_print(self, json_dict):
        """Pretty print the logging message."""
        if self.prettyprint:
            return '\n' + json.dumps(json_dict, indent=self.indent)
        return json.dumps(json_dict)


class SimpleLogRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    """A class to handle log requests."""

    def __init__(self, request, client_address, server, app_name='SimpleAciUiLogServer'):
        """Initialize an instance of this class."""
        BaseHTTPServer.BaseHTTPRequestHandler.__init__(self, request, client_address, server)
        self._log_paths = None
        self._app_name = app_name
        return

    @property
    def log_paths(self):
        """A property to return log_paths."""
        return self._log_paths

    @log_paths.setter
    def log_paths(self, value):
        """A property to set log_paths."""
        self._log_paths = value

    @property
    def app_name(self):
        """A property to get app_name."""
        return self._app_name

    @app_name.setter
    def app_name(self, value):
        """A property to set app_name."""
        self._app_name = value

    def is_log_path_valid(self):
        """Make sure the log_paths is valid."""
        if self.log_paths:
            return self.path in self.log_paths
        else:
            return True

    def send_200_resp(self, response, content_type):
        """Send a HTTP 200 (OK) response."""
        self.send_response(200)
        self.send_header('Content-type', content_type)
        if response is not None:
            resplen = str(len(response))
        else:
            resplen = 0
        self.send_header('Content-length', resplen)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        if response is not None:
            self.wfile.write(response)
        return

    def do_GET(self):
        """Handle HTTP GET requests.

        Simply returns a small amount of info so you can tell the server is
        functioning.
        """
        if not self.is_log_path_valid():
            self.report_404()
            return
        else:
            scheme = 'https' if self.server.cert is not None else 'http'
            resp = '<html>'
            resp += '<head>\n'
            resp += ('  <title>{0}</title>\n').format(self.app_name)
            resp += '</head>\n'
            resp += '<body>\n'
            resp += '  <center>\n'
            resp += ('    <h2>{0} is working via {1}</h2>\n').format(self.app_name, scheme.upper())
            resp += '  </center>\n'
            resp += '  <p>Please point your APIC at:<br /><br />'
            ip_add = [ (s.connect((self.client_address[0], 80)), s.getsockname()[0], s.close()) for s in [
             socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]
                     ][0][1]
            resp += ('      {0}://{1}:{2}{3}</p>').format(scheme, ip_add, self.server.server_address[1], self.path)
            resp += '</body>\n'
            resp += '</html>'
            self.send_200_resp(resp, 'text/html')
            return

    def do_POST(self):
        """Handle HTTP/S POST requests.

        Attempts to interpret all HTTP POST requests as Log calls,
        which are forwarded to the server's _dispatch method for handling.
        """
        if not self.is_log_path_valid():
            self.report_404()
            return
        else:
            try:
                max_chunk_size = 10485760
                size_remaining = int(self.headers['content-length'])
                chunk_list = []
                while size_remaining:
                    chunk_size = min(size_remaining, max_chunk_size)
                    chunk = self.rfile.read(chunk_size)
                    if not chunk:
                        break
                    chunk_list.append(chunk)
                    size_remaining -= len(chunk_list[(-1)])

                data = ('').join(chunk_list)
                data = self.decode_request_content(StringIO(data))
                if data is None:
                    return
                if 'data' in data.keys() and 'method' in data['data'].keys():
                    response = self.server.dispatch(data['data']['method'], data)
                else:
                    response = None
            except Exception:
                self.send_response(500)
                raise
            else:
                self.send_200_resp(response, 'text/plain')

            return

    @staticmethod
    def extract_form_fields(item):
        """Extract form fields from a POST."""
        formitems = item.value.rstrip('\r\n')
        itemlist = formitems.split('\n')
        re_list = [
         re.compile('^[0-1][0-9]:[0-5][0-9]:[0-5][0-9] DEBUG - $'),
         re.compile('^(payload)({".*)$'),
         re.compile('^([a-z]+): (.*)$')]
        itemdict = {}
        for anitem in itemlist:
            for a_re in re_list:
                match = re.search(a_re, anitem)
                if match:
                    if len(match.groups()) == 0:
                        itemdict['preamble'] = match.group(0)
                    elif len(match.groups()) == 2:
                        itemdict[match.group(1)] = match.group(2)
                    continue

        return itemdict

    def decode_request_content(self, datafile):
        """Decode the request content based on content-type."""
        content_type = self.headers.get('Content-Type', 'notype').lower()
        if 'application/x-www-form-urlencoded' in content_type:
            form = cgi.FieldStorage(fp=datafile, headers=self.headers, environ=dict(REQUEST_METHOD='POST', CONTENT_TYPE=self.headers['Content-Type']))
            itemdict = {}
            for item in form.list:
                if item.name == 'data':
                    itemdict['data'] = SimpleLogRequestHandler.extract_form_fields(item)
                elif item.name == 'layout':
                    itemdict['layout'] = item.value

            return itemdict
        self.send_response(501, 'Content-Type %r not supported' % content_type)
        self.send_header('Content-length', '0')
        self.end_headers()
        return

    def report_404(self):
        """Report a HTTP 404 error."""
        self.send_response(404)
        response = 'No such page'
        self.send_header('Content-type', 'text/plain')
        self.send_header('Content-length', str(len(response)))
        self.end_headers()
        self.wfile.write(response)

    def log_request(self, code='-', size='-'):
        """Selectively log an accepted request."""
        if self.server.log_requests:
            BaseHTTPServer.BaseHTTPRequestHandler.log_request(self, code, size)


class SimpleAciUiLogServer(SocketServer.TCPServer, SimpleLogDispatcher):
    """A simple server to handle ACI UI logging."""
    allow_reuse_address = True
    _send_traceback_header = False

    def __init__(self, addr, cert=None, request_handler=SimpleLogRequestHandler, log_requests=False, allow_none=False, bind_and_activate=True, location=None, excludes=None, app_name='SimpleAciUiLogServer', request_types=None):
        """Initialize an instance of this class."""
        self.log_requests = log_requests
        self._cert = cert
        self.daemon = True
        if excludes is None:
            excludes = []
        if location is not None:
            if not location.startswith('/'):
                location = '/' + str(location)
            request_handler.log_paths = [
             location]
        request_handler.app_name = app_name
        if request_types is None:
            request_types = [
             'all']
        SimpleLogDispatcher.__init__(self, allow_none=allow_none, excludes=excludes, request_types=request_types)
        SocketServer.TCPServer.__init__(self, addr, request_handler, bind_and_activate)
        if fcntl is not None and hasattr(fcntl, 'FD_CLOEXEC'):
            flags = fcntl.fcntl(self.fileno(), fcntl.F_GETFD)
            flags |= fcntl.FD_CLOEXEC
            fcntl.fcntl(self.fileno(), fcntl.F_SETFD, flags)
        if self._cert:
            self.socket = ssl.wrap_socket(self.socket, certfile=self.cert, server_side=True)
        return

    @property
    def cert(self):
        """The name of the file containing the server certificate for https."""
        return self._cert

    @cert.setter
    def cert(self, value):
        """Set the name of the file with the server certificate for https."""
        self._cert = value


class ThreadingSimpleAciUiLogServer(SocketServer.ThreadingMixIn, SimpleAciUiLogServer):
    """Threading SimpleAciUiLogServer.

    Prevent concurrent connections do not block.
    """
    pass


def serve_forever(servers, poll_interval=0.5):
    """Handle n number of threading servers.

    For non-threading servers simply use the native server_forever function.
    """
    while True:
        ready, wait, excep = select.select(servers, [], [], poll_interval)
        for server in servers:
            if server in ready:
                server.handle_request()


def main():
    """The main function for when this is run as a standalone script."""
    cert = ''

    def sigint_handler(sig, frame):
        """Handle interrupt signals."""
        if not args.cert:
            try:
                os.unlink(cert)
            except OSError:
                pass

        print 'Exiting...'
        sys.exit(0)

    parser = ArgumentParser('Remote APIC API Inspector and GUI Log Server')
    parser.add_argument('-a', '--apicip', required=False, default='8.8.8.8', help='If you have a multihomed system, where the ' + 'apic is on a private network, the server will ' + 'print the ip address your local system has a ' + 'route to 8.8.8.8.  If you want the server to ' + 'print a more accurate ip address for the ' + 'server you can tell it the apicip address.')
    parser.add_argument('-c', '--cert', type=str, required=False, help='The server certificate file for ssl ' + 'connections, default="server.pem"')
    parser.add_argument('-d', '--delete_imdata', action='store_true', default=False, required=False, help='Strip the imdata from the response and payload')
    parser.add_argument('-e', '--exclude', action='append', nargs='*', default=[], choices=['subscriptionRefresh',
     'aaaRefresh',
     'aaaLogout',
     'HDfabricOverallHealth5min-0',
     'topInfo', 'all'], help='Exclude certain types of common noise queries.')
    parser.add_argument('-i', '--indent', type=int, default=2, required=False, help='The number of spaces to indent when pretty ' + 'printing')
    parser.add_argument('-l', '--location', default='/apiinspector', required=False, help='Location that transaction logs are being ' + 'sent to, default=/apiinspector')
    parser.add_argument('-n', '--nice-output', action='store_true', default=False, required=False, help='Pretty print the response and payload')
    parser.add_argument('-p', '--port', type=int, required=False, default=8987, help='Local port to listen on, default=8987')
    parser.add_argument('-s', '--sslport', type=int, required=False, default=8443, help='Local port to listen on for ssl connections, ' + 'default=8443')
    parser.add_argument('-r', '--requests-log', action='store_true', default=False, required=False, help='Log server requests and response codes to ' + 'standard error')
    parser.add_argument('-t', '--title', default='SimpleAciUiLogServer', required=False, help='Change the name shown for this application ' + 'when accessed with a GET request')
    parser.add_argument('-ty', '--type', action='append', nargs='*', default=[
     'all'], choices=['POST', 'GET', 'undefined',
     'EventChannelMessage'], help='Limit logs to specific request types.')
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s - \n%(message)s')
    if args.exclude:
        args.exclude = [ val for sublist in args.exclude for val in sublist ]
    if not args.location.startswith('/'):
        args.location = '/' + str(args.location)
    if args.type:
        args.type = [ val for sublist in args.type for val in sublist ]
    ThreadingSimpleAciUiLogServer.prettyprint = args.nice_output
    ThreadingSimpleAciUiLogServer.indent = args.indent
    ThreadingSimpleAciUiLogServer.strip_imdata = args.delete_imdata
    http_server = ThreadingSimpleAciUiLogServer(('', args.port), log_requests=args.requests_log, location=args.location, excludes=args.exclude, app_name=args.title)
    if not args.cert:
        cert_file = tempfile.NamedTemporaryFile(delete=False)
        cert_file.write(SERVER_CERT)
        cert_file.close()
        cert = cert_file.name
        print '\n+++WARNING+++ Using an embedded self-signed certificate for ' + 'HTTPS, this is not secure.\n'
    else:
        cert = args.cert
    https_server = ThreadingSimpleAciUiLogServer(('', args.sslport), cert=cert, location=args.location, log_requests=args.requests_log, excludes=args.exclude, app_name=args.title)
    signal.signal(signal.SIGINT, sigint_handler)
    ip_add = [ (s.connect((args.apicip, 80)), s.getsockname()[0], s.close()) for s in [
     socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]
             ][0][1]
    print 'Servers are running and reachable via:\n'
    print 'http://' + str(ip_add) + ':' + str(args.port) + args.location
    print 'https://' + str(ip_add) + ':' + str(args.sslport) + args.location + '\n'
    print 'Make sure your APIC(s) are configured to send log messages: ' + 'welcome username -> Start Remote Logging'
    print 'Note: If you connect to your APIC via HTTPS, configure the ' + 'remote logging to use the https server.'
    serve_forever([http_server, https_server])


if __name__ == '__main__':
    main()