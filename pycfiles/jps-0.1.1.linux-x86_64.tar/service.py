# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/jps/service.py
# Compiled at: 2016-06-11 06:32:43
import zmq
from zmq.utils.strtypes import cast_bytes
import threading
from .common import DEFAULT_RES_PORT
from .common import DEFAULT_REQ_PORT
from .env import get_master_host

class ServiceServer(object):
    """
    Example:

    >>> def callback(req):
    ...   return 'req = {req}'.format(req=req)
    ...
    >>> service = jps.ServiceServer(callback)
    >>> service.spin()
    """

    def __init__(self, callback, host=None, res_port=DEFAULT_RES_PORT):
        if host is None:
            host = get_master_host()
        context = zmq.Context()
        self._socket = context.socket(zmq.REP)
        self._socket.connect(('tcp://{host}:{port}').format(host=host, port=res_port))
        self._callback = callback
        self._thread = None
        return

    def spin(self, use_thread=False):
        r"""call callback for all data forever (until \C-c)

        :param use_thread: use thread for spin (do not block)
        """
        if use_thread:
            if self._thread is not None:
                raise 'spin called twice'
            self._thread = threading.Thread(target=self._spin_internal)
            self._thread.setDaemon(True)
            self._thread.start()
        else:
            self._spin_internal()
        return

    def _spin_internal(self):
        while True:
            self.spin_once()

    def spin_once(self):
        request = self._socket.recv()
        self._socket.send(cast_bytes(self._callback(request)))


class ServiceClient(object):

    def __init__(self, host=None, req_port=DEFAULT_REQ_PORT):
        if host is None:
            host = get_master_host()
        context = zmq.Context()
        self._socket = context.socket(zmq.REQ)
        self._socket.connect(('tcp://{host}:{port}').format(host=host, port=req_port))
        return

    def call(self, request):
        self._socket.send(request)
        return self._socket.recv()

    __call__ = call