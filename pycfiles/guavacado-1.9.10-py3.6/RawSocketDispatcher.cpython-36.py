# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/guavacado/RawSocketDispatcher.py
# Compiled at: 2019-06-28 16:24:29
# Size of source mod 2**32: 380 bytes
from .misc import init_logger

class RawSocketDispatcher(object):
    __doc__ = 'a dispatcher to simply call a callback function on each connection'

    def __init__(self, callback):
        self.log_handler = init_logger(__name__)
        self.callback = callback

    def handle_connection(self, clientsocket, address, client_id):
        self.callback(clientsocket, address, client_id)