# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/guavacado/ConnDispatcher.py
# Compiled at: 2019-06-30 17:19:43
# Size of source mod 2**32: 1880 bytes
from .misc import init_logger, addr_rep
from .ConnListener import ConnListener
import os, threading

class ConnDispatcher(object):
    __doc__ = 'handles dispatching connections from multiple ConnListener instances to the proper callback functions'

    def __init__(self):
        self.log_handler = init_logger(__name__)
        self.conn_listeners = {}

    def get_conn_listener(self, name):
        return self.conn_listeners[name]

    def add_conn_listener(self, addr, conn_handler, name=None):
        if name is None:
            name = 'gen_conn_listener_' + str(addr)

        def handle_callback(clientsocket, address, client_id, name=name):
            self.conn_listeners[name]['handler'](clientsocket, address, client_id)

        self.conn_listeners[name] = {'listener':ConnListener(handle_callback, addr=addr),  'handler':conn_handler,  'addr':addr}
        return name

    def start_service(self):
        for listener_name in self.conn_listeners:
            listener = self.conn_listeners[listener_name]
            self.log_handler.debug('Starting connection listener for {addr}'.format(addr=(addr_rep(listener['addr']))))
            listener['thread'] = threading.Thread(target=(listener['listener'].run), name='conn_listener_{addr}'.format(addr=(addr_rep(listener['addr']))))
            listener['thread'].daemon = True
            listener['thread'].start()

    def stop_service(self):
        for listener_name in self.conn_listeners:
            listener = self.conn_listeners[listener_name]
            self.log_handler.debug('Stopping connection listener for {addr}'.format(addr=(addr_rep(listener['addr']))))
            listener['listener'].stop()
            listener['thread'].join(60)
            if listener['thread'].is_alive():
                self.log_handler.warn('Continuing without closing connection listener thread for {addr} because it did not close!'.format(addr=(addr_rep(listener['addr']))))
            else:
                self.log_handler.debug('Stopped connection listener for {addr}'.format(addr=(addr_rep(listener['addr']))))