# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/guavacado/Client.py
# Compiled at: 2019-07-25 22:56:26
# Size of source mod 2**32: 5587 bytes
import socket, ssl, threading
from .misc import addr_rep, init_logger
from .WebRequestHandler import WebRequestHandler

class Client(object):
    __doc__ = '\n\tallows connections to be made as a client\n\t'

    def __init__(self, addr='localhost', port=80, TLS=False, UDP=False, disp_type='web', TLS_check_cert=True):
        self.log_handler = init_logger(__name__)
        self.addr = addr
        self.port = port
        self.TLS = TLS
        self.UDP = UDP
        self.disp_type = disp_type
        self.TLS_check_cert = TLS_check_cert

    @staticmethod
    def from_url(url, TLS_check_cert=True):
        prot_split = url.split('://', 1)
        if len(prot_split) > 1:
            protocol = prot_split[0]
            url_noprot = prot_split[1]
        else:
            protocol = 'http'
            url_noprot = url
        if protocol.lower() in ('https', ):
            TLS = True
        else:
            TLS = False
        host_port_split = url_noprot.split('/', 1)
        if len(host_port_split) > 1:
            host_port = host_port_split[0]
            resource = '/' + host_port_split[1]
        else:
            host_port = url_noprot
            resource = '/'
        host_split = host_port.split(':', 1)
        if len(host_split) > 1:
            host = host_split[0]
            try:
                port = int(host_split[1])
            except ValueError:
                host = host_port
                if TLS:
                    port = 443
                else:
                    port = 80

        else:
            host = host_port
            if TLS:
                port = 443
            else:
                port = 80
            return (Client(addr=host, port=port, TLS=TLS, disp_type='web', TLS_check_cert=TLS_check_cert), resource)

    @staticmethod
    def request_url(url, method='GET', body=None, TLS_check_cert=True):
        c, r = Client.from_url(url, TLS_check_cert=TLS_check_cert)
        return c.request_web(resource=r, method=method, body=body)

    def connect_socket(self):
        """creates a socket connection to the server"""
        self.log_handler.debug('making connection to {addr}.'.format(addr=(addr_rep({'addr':self.addr,  'port':self.port,  'TLS':self.TLS,  'UDP':self.UDP}))))
        if self.TLS:
            tls_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            if self.TLS_check_cert:
                tls_context.verify_mode = ssl.CERT_REQUIRED
                tls_context.check_hostname = True
            else:
                tls_context.check_hostname = False
                tls_context.verify_mode = ssl.CERT_NONE
            tls_context.load_default_certs()
            raw_sock = socket.socket(socket.AF_INET)
            sock = tls_context.wrap_socket(raw_sock, server_hostname=(self.addr))
        else:
            if self.UDP:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            else:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.addr, self.port))
        return sock

    def close_socket(self, sock):
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()

    def request_web(self, resource='/', method='GET', body=None):
        """makes a web request and returns the body of the response"""
        ret = []
        ret_event = threading.Event()

        def req_callback(body, code, ret=ret, ret_event=ret_event):
            ret.append((body, code))
            ret_event.set()

        self.request_web_async(req_callback, resource=resource, method=method, body=body)
        ret_event.wait()
        return ret[0]

    def request_web_async(self, callback, resource='/', method='GET', body=None, timeout=None):
        """makes a web request using the raw socket and returns the body of the response"""
        sock = self.connect_socket()
        req_handler = WebRequestHandler(sock, (self.addr, self.port), None, callback, timeout=timeout, is_client=True, client_resource=resource, client_body=body, client_method=method, client_host=(self.addr))
        req_handler.handle_connection()