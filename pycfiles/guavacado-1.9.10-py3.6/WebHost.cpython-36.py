# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/guavacado/WebHost.py
# Compiled at: 2020-04-06 14:04:36
# Size of source mod 2**32: 3543 bytes
from .WebDocs import WebDocs
from .WebFileInterface import WebFileInterface
from .ConnDispatcher import ConnDispatcher
from .misc import init_logger, set_loglevel, addr_rep
from .WebDispatcher import WebDispatcher
from .RedirectDispatcher import RedirectDispatcher
from .RawSocketDispatcher import RawSocketDispatcher

class WebHost(object):
    __doc__ = '\n\t\tclass for hosting a "/static" folder\n\t\tallows WebInterface objects to serve dynamic content alongside the "/static" folder\n\t'

    def __init__(self, timeout=10, loglevel='INFO', error_404_page_func=None):
        set_loglevel(loglevel)
        self.log_handler = init_logger(__name__)
        self.addr = []
        self.timeout = timeout
        self.error_404_page_func = error_404_page_func
        self.specialized_dispatchers = {}
        self.dispatcher = ConnDispatcher()
        self.docs = WebDocs(self)
        self.docs.connect_funcs()

    def add_addr(self, addr=None, port=80, TLS=None, UDP=False, disp_type='web'):
        """
                adds an address to the dispatcher for it to listen on
                addr should be a hostname to listen on, or None to listen on all addresses
                port should be a port number to listen on
                TLS should be a tuple of two filenames to use for the certfile and keyfile for TLS, or None to use plain HTTP
                """
        addr_tuple = (
         (
          addr, port), TLS)
        addr_dict = {'addr':addr,  'port':port,  'TLS':TLS,  'UDP':UDP}
        self.addr.append(addr_dict)
        self.dispatcher.add_conn_listener(addr_dict, (self.get_specialized_dispatcher(disp_type).handle_connection), name=('WebDispatch_' + addr_rep(addr_dict)))

    def start_service(self):
        if len(self.addr) == 0:
            self.log_handler.warn('No port number specified! Defaulting to port 80!')
            self.add_addr()
        self.log_handler.info('Starting web server on {addr}'.format(addr=(addr_rep(self.addr))))
        self.log_handler.debug('All Resources: {}'.format(self.get_docs().GET_DOCS_JSON()))
        self.dispatcher.start_service()

    def stop_service(self):
        self.log_handler.info('Stopping web server on {addr}'.format(addr=(addr_rep(self.addr))))
        self.dispatcher.stop_service()
        self.log_handler.info('Web server stopped on {addr}'.format(addr=(addr_rep(self.addr))))

    def get_dispatcher(self):
        return self.dispatcher

    def get_specialized_dispatcher(self, disp_type):

        def setup_web_dispatcher(ident=None, auth=None):
            return WebDispatcher(addr=(self.addr), timeout=(self.timeout), error_404_page_func=(self.error_404_page_func), auth_handler=auth)

        def setup_redirect_dispatcher(target_domain):
            return RedirectDispatcher(timeout=(self.timeout), target_domain=target_domain)

        def setup_raw_socket_dispatcher(callback):
            return RawSocketDispatcher(callback)

        dispatcher_setup_funcs = {'web':setup_web_dispatcher, 
         'redirect':setup_redirect_dispatcher, 
         'raw_socket':setup_raw_socket_dispatcher}
        if disp_type in self.specialized_dispatchers:
            return self.specialized_dispatchers[disp_type]
        elif type(disp_type) in [tuple, list] and type(disp_type[0]) in [str]:
            disp_type_string = disp_type[0]
            disp_args = disp_type[1:]
        else:
            disp_type_string = disp_type
            disp_args = ()
        if disp_type_string in dispatcher_setup_funcs:
            disp = (dispatcher_setup_funcs[disp_type_string])(*disp_args)
            self.specialized_dispatchers[disp_type] = disp
            return disp
        raise NotImplementedError('Dispatcher type "{}" is not implemented!'.format(disp_type))

    def get_docs(self):
        return self.docs

    def get_addr(self):
        return self.addr