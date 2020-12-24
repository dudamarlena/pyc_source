# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/pituophis/__init__.py
# Compiled at: 2019-05-24 19:24:47
# Size of source mod 2**32: 25186 bytes
import asyncio, glob, mimetypes, os, re, socket, ssl
from operator import itemgetter
from os.path import realpath
from urllib.parse import urlparse
from natsort import natsorted

class Response:
    __doc__ = '\n    *Client.* Returned by Request.get() and get(). Represents a received binary object from a Gopher server.\n    '

    def __init__(self, stream):
        """
        Reads a BufferedReader to the object's binary property and initializes a new Response object.
        """
        self.binary = stream.read()

    def text(self):
        """
        Returns the binary decoded as a UTF-8 String.
        """
        return self.binary.decode('utf-8')

    def menu(self):
        """
        Decodes the binary as text and parses it as a Gopher menu. Returns a List of Gopher menu items parsed as the Selector type.
        """
        return parse_menu(self.binary.decode('utf-8'))


class Request:
    __doc__ = '\n    *Client/Server.* Represents a request to be sent to a Gopher server, or received from a client.\n    '

    def __init__(self, host='127.0.0.1', port=70, advertised_port=None, path='/', query='', itype='9', tls=False, tls_verify=True, client='', pub_dir='pub/', alt_handler=False):
        """
        Initializes a new Request object.
        """
        self.host = str(host)
        self.port = int(port)
        if advertised_port is None:
            advertised_port = self.port
        self.advertised_port = int(advertised_port)
        self.path = str(path)
        self.query = str(query)
        self.type = str(itype)
        self.tls = tls
        self.tls_verify = tls_verify
        self.client = str(client)
        self.pub_dir = str(pub_dir)
        self.alt_handler = alt_handler

    def get(self):
        """
        *Client.* Sends the Request and returns a Response object.
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.host.count(':') > 1:
            s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        else:
            if self.tls:
                context = ssl._create_unverified_context()
                if self.tls_verify:
                    context = ssl.create_default_context()
                s = context.wrap_socket(s, server_hostname=(self.host))
            else:
                s.settimeout(10.0)
            s.connect((self.host.replace('[', '').replace(']', ''),
             int(self.port)))
            if self.query == '':
                msg = self.path + '\r\n'
            else:
                msg = self.path + '\t' + self.query + '\r\n'
        s.sendall(msg.encode('utf-8'))
        return Response(s.makefile('rb'))

    def url(self):
        """
        Returns a URL equivalent to the Request's properties.
        """
        protocol = 'gopher'
        if self.tls:
            protocol = 'gophers'
        path = self.path
        if not path.startswith('/'):
            path = '/' + path
        query = ''
        if not self.query == '':
            query = '?' + self.query
        return protocol + '://' + str(self.host) + ':' + str(self.port) + '/' + str(self.type) + str(path) + str(query)


class Selector:
    __doc__ = '\n    *Server/Client.* Represents a selector in a parsed Gopher menu.\n    '

    def __init__(self, itype='i', text='', path='/', host='error.host', port=0, tls=False):
        """
        Initializes a new Selector object.
        """
        self.type = itype
        self.text = text
        self.path = path
        self.host = host
        self.port = port
        self.tls = tls

    def source(self):
        """
        Returns a representation of what the selector looks like in a Gopher menu.
        """
        port = int(self.port)
        if self.tls:
            while len(str(port)) < 5:
                port = '0' + str(port)

            port = '1' + str(port)
            port = int(port)
        return str(self.type) + str(self.text) + '\t' + str(self.path) + '\t' + str(self.host) + '\t' + str(port) + '\r\n'

    def request(self):
        """
        Returns a Request equivalent to where the selector leads.
        """
        req = Request()
        req.type = self.type
        req.host = self.host
        req.port = self.port
        req.path = self.path
        if '?' in req.path:
            req.query = '%3F'.join(req.path.split('?')[-1:])
            req.path = req.path.split('?')[0]
        req.tls = self.tls
        return req


def parse_menu(source):
    """
    *Client.* Parses a String as a Gopher menu. Returns a List of Selectors.
    """
    parsed_menu = []
    menu = source.replace('\r\n', '\n').replace('\n', '\r\n').split('\r\n')
    for line in menu:
        selector = Selector()
        if line.startswith('i'):
            selector.type = 'i'
            selector.text = line[1:].split('\t')[0]
            selector.path = '/'
            selector.host = 'error.host'
            selector.port = 0
        else:
            line = line.split('\t')
            while len(line) > 4:
                line = line[:-1]

            line = '\t'.join(line)
            matches = re.match('^(.)(.*)\\t(.*)\\t(.*)\\t(.*)', line)
            if matches:
                selector.type = matches[1]
                selector.text = matches[2]
                selector.path = matches[3]
                selector.host = matches[4]
                selector.port = matches[5]
                try:
                    selector.port = int(selector.port)
                except:
                    selector.port = 70

                if selector.port > 65535:
                    selector.tls = True
                    selector.port = int(str(selector.port)[1:])
            parsed_menu.append(selector)

    return parsed_menu


def parse_url(url):
    """
    *Client.* Parses a Gopher URL and returns an equivalent Request.
    """
    req = Request(host='', port=70, path='/', query='', tls=False)
    up = urlparse(url)
    if up.scheme == '':
        up = urlparse('gopher://' + url)
    else:
        if up.scheme == 'gophers':
            req.tls = True
        req.query = up.query
        if up.netloc == '':
            if '/' in up.path:
                req.host = up.path.split('/')[0]
                try:
                    req.path = '/'.join(up.path.split('/')[:-1])
                except Exception:
                    req.path = '/'

            else:
                req.host = up.path
                req.path = '/'
        else:
            req.host = up.netloc
        req.path = up.path
    if ':' in re.sub('\\[.*\\]', '', req.host):
        req.port = req.host.split(':')[(-1)]
        req.host = ':'.join(req.host.split(':')[:-1])
    ps = req.path.split('/')
    if len(ps) > 1:
        if len(ps[1]) == 1:
            req.type = ps.pop(1)
            req.path = '/'.join(ps)
    if req.path.endswith('/'):
        req.type = '1'
    return req


def get(host, port=70, path='/', query='', tls=False, tls_verify=True):
    """
    *Client.* Quickly creates and sends a Request. Returns a Response object.
    """
    req = Request(host=host, port=port, path=path, query=query, tls=tls, tls_verify=tls_verify)
    if '/' in host or ':' in host:
        req = parse_url(host)
    return req.get()


mime_starts_with = {'image':'I', 
 'text':'0', 
 'audio/x-wav':'s', 
 'image/gif':'g', 
 'text/html':'h'}

def parse_gophermap(source, def_host='127.0.0.1', def_port='70', gophermap_dir='/', pub_dir='pub/', tls=False):
    """
    *Server.* Converts a Bucktooth-style Gophermap (as a String or List) into a Gopher menu as a List of Selectors to send.
    """
    if not gophermap_dir.endswith('/'):
        gophermap_dir += '/'
    if not pub_dir.endswith('/'):
        pub_dir += '/'
    if type(source) == str:
        source = source.replace('\r\n', '\n').split('\n')
    new_menu = []
    for selector in source:
        if '\t' in selector:
            selector = selector.split('\t')
            expanded = False
            itype = selector[0][0]
            text = selector[0][1:]
            path = gophermap_dir + text
            if itype == '1':
                path += '/'
            host = def_host
            port = def_port
            if len(selector) > 1:
                path = selector[1]
            if len(selector) > 2:
                host = selector[2]
            if len(selector) > 3:
                port = selector[3]
            if path == '':
                path = gophermap_dir + text
                if itype == '1':
                    path += '/'
            if not path.startswith('URL:'):
                if not path.startswith('/'):
                    path = realpath(gophermap_dir + '/' + path)
                if '*' in path:
                    expanded = True
                    if os.path.abspath(pub_dir) in os.path.abspath(pub_dir + path):
                        g = natsorted(glob.glob(pub_dir + path))
                        listing = []
                        for file in g:
                            file = re.sub('/{2}', '/', file)
                            s = Selector()
                            s.type = itype
                            if s.type == '?':
                                s.type = '9'
                                if path.startswith('URL:'):
                                    s.type = 'h'
                                else:
                                    if os.path.exists(file):
                                        mime = mimetypes.guess_type(file)[0]
                                        if mime is None:
                                            if os.path.isdir(file):
                                                s.type = '1'
                                            else:
                                                s.type = '9'
                                                if file.endswith('.md'):
                                                    s.type = 1
                                        else:
                                            for sw in mime_starts_with.keys():
                                                if mime.startswith(sw):
                                                    s.type = mime_starts_with[sw]

                                    else:
                                        splt = file.split('/')
                                        while '' in splt:
                                            splt.remove('')

                                        s.text = splt[(len(splt) - 1)]
                                        if os.path.exists(file + '/gophertag'):
                                            s.text = ''.join(list(open(file + '/gophertag'))).replace('\r\n', '').replace('\n', '')
                                        s.path = file.replace(pub_dir, '/', 1)
                                        s.path = re.sub('/{2}', '/', s.path)
                                        s.host = host
                                        s.port = port
                                        if s.type == 'i':
                                            s.path = ''
                                            s.host = 'error.host'
                                            s.port = '0'
                                        if s.type == '1':
                                            d = 0
                                        else:
                                            d = 1
                                    s.path.endswith('gophermap') or s.path.endswith('gophertag') or listing.append([
                                     file, s, s.text, d])

                        listing = natsorted(listing, key=(itemgetter(0)))
                        listing = natsorted(listing, key=(itemgetter(2)))
                        listing = natsorted(listing, key=(itemgetter(3)))
                        for item in listing:
                            new_menu.append(item[1])

        else:
            new_menu.append(Selector(itype='3', text='403: Gopher glob out of scope.'))
        if not expanded:
            selector = Selector()
            selector.type = itype
            selector.text = text
            selector.path = path
            selector.host = host
            selector.port = port
            if selector.type == '?':
                selector.type = '9'
                if path.startswith('URL:'):
                    selector.type = 'h'
                else:
                    if os.path.exists(pub_dir + path):
                        mime = mimetypes.guess_type(pub_dir + path)[0]
                        if mime is None:
                            if os.path.isdir(file):
                                s.type = '1'
                    else:
                        s.type = '9'
            else:
                for sw in mime_starts_with.keys():
                    if mime.startswith(sw):
                        selector.type = mime_starts_with[sw]

            if selector.host == def_host:
                if selector.port == def_port:
                    selector.tls = tls
                new_menu.append(selector.source())
            else:
                selector = 'i' + selector + '\t\terror.host\t0'
                new_menu.append(selector)

    return new_menu


def handle(request):
    """
    *Server.* Default handler function for Gopher requests while hosting a server.
    Serves files and directories from the pub/ directory by default, but the path can
    be changed in serve's pub_dir argument or changing the Request's pub_dir directory.
    """
    pub_dir = request.pub_dir
    errors = {'404':Selector(itype='3', text='404: ' + request.path + ' does not exist'), 
     '403':Selector(itype='3', text='403: Resource outside of publish directory'), 
     'no_pub_dir':Selector(itype='3', text='500: Publish directory does not exist')}
    if request.advertised_port is None:
        request.advertised_port = request.port
    else:
        if request.path.startswith('URL:'):
            html = '\n        <!DOCTYPE html>\n        <html>\n        <head>\n            <title>Gopher Redirect</title>\n            <meta http-equiv="refresh" content="0; url=[#url#]" />\n        </head>\n        <body>\n            <h1>Gopher Redirect</h1>\n            <p>You will be redirected to <a href="[#url#]">[#url#]</a> shortly.</p>\n        </body>\n        '
            return html.replace('[#url#]', request.path.split('URL:')[1])
        return os.path.exists(pub_dir) or [
         errors['no_pub_dir']]
    menu = []
    if request.path == '':
        request.path = '/'
    else:
        res_path = os.path.abspath((pub_dir + request.path).replace('//', '/'))
        if not res_path.startswith(os.path.abspath(pub_dir)):
            return [errors['403']]
        if os.path.isdir(res_path):
            if os.path.exists(res_path):
                if os.path.isfile(res_path + '/gophermap'):
                    in_file = open(res_path + '/gophermap', 'r+')
                    gmap = in_file.read()
                    in_file.close()
                    menu = parse_gophermap(source=gmap, def_host=(request.host),
                      def_port=(request.advertised_port),
                      gophermap_dir=(request.path),
                      pub_dir=pub_dir,
                      tls=(request.tls))
                else:
                    gmap = '?*\t\r\n'
                    menu = parse_gophermap(source=gmap, def_host=(request.host),
                      def_port=(request.advertised_port),
                      gophermap_dir=(request.path),
                      pub_dir=pub_dir,
                      tls=(request.tls))
            else:
                if request.alt_handler:
                    alt = request.alt_handler(request)
                    if alt:
                        return alt
                    return [errors['404']]
                else:
                    return [
                     errors['404']]
        else:
            if os.path.isfile(res_path):
                in_file = open(res_path, 'rb')
                data = in_file.read()
                in_file.close()
                return data
                if request.alt_handler:
                    alt = request.alt_handler(request)
                    if alt:
                        return alt
                    return [errors['404']]
            else:
                return [
                 errors['404']]
    return menu


def serve(host='127.0.0.1', port=70, advertised_port=None, handler=handle, pub_dir='pub/', alt_handler=False, send_period=False, tls=False, tls_cert_chain='cacert.pem', tls_private_key='privkey.pem', debug=True):
    """
    *Server.*  Listens for Gopher requests. Allows for using a custom handler that will return a Bytes, String, or List
    object (which can contain either Strings or Selectors) to send to the client, or the default handler which can serve
    a directory. Along with the default handler, you can set an alternate handler to use if a 404 error is generated for
    dynamic applications.
    """
    if tls:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        if os.path.exists(tls_cert_chain) and os.path.exists(tls_private_key):
            context.load_cert_chain(tls_cert_chain, tls_private_key)
        else:
            print('TLS certificate and/or private key is missing. TLS has been disabled for this session.')
            print('Run this command to generate a self-signed certificate and private key:')
            print('  openssl req -x509 -newkey rsa:4096 -keyout "' + tls_private_key + '" -out "' + tls_cert_chain + '" -days 365')
            print('Note that clients might refuse to connect to a self-signed certificate.')
            print()
            tls = False
    elif tls:
        print('S/Gopher server is now running on', host + ':' + str(port) + '.')
    else:
        print('Gopher server is now running on', host + ':' + str(port) + '.')

    class GopherProtocol(asyncio.Protocol):

        def connection_made(self, transport):
            self.transport = transport
            print('Connected by', transport.get_extra_info('peername'))

        def data_received(self, data):
            request = data.decode('utf-8').split('\t')
            path = request[0].replace('\r\n', '')
            query = ''
            if len(request) > 1:
                query = request[1].replace('\r\n', '')
            if debug:
                print('Client requests:', path, query)
            is_tls = False
            if self.transport.get_extra_info('sslcontext'):
                is_tls = True
            resp = handler(Request(path=path, query=query, host=host, port=port,
              advertised_port=advertised_port,
              client=(self.transport.get_extra_info('peername')[0]),
              pub_dir=pub_dir,
              alt_handler=alt_handler,
              tls=is_tls))
            if type(resp) == str:
                resp = bytes(resp, 'utf-8')
            else:
                if type(resp) == list:
                    out = ''
                    for line in resp:
                        if type(line) == str:
                            line = line.replace('\r\n', '\n')
                            line = line.replace('\n', '\r\n')
                            if not line.endswith('\r\n'):
                                line += '\r\n'
                            out += line
                        if type(line) == Selector:
                            out += line.source()

                    resp = bytes(out, 'utf-8')
                self.transport.write(resp)
                if send_period:
                    self.transport.write(b'.')
                self.transport.close()
                if debug:
                    print('Connection closed')

    async def main(h, p):
        loop = asyncio.get_running_loop()
        if tls:
            server = await loop.create_server(GopherProtocol, h, p, ssl=context)
        else:
            server = await loop.create_server(GopherProtocol, h, p)
        await server.serve_forever()

    asyncio.run(main('0.0.0.0', port))