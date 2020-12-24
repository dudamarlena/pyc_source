# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/zerolog/worker.py
# Compiled at: 2016-09-30 02:06:36
# Size of source mod 2**32: 1740 bytes
"""Base worker implmentation"""
import logging, zmq
log = logging.getLogger(__name__)

class BaseWorker:
    __doc__ = 'Base worker class.\n\n    This class cannot be used "as is", it will raises an ``ImplementationError`` in ``process_data`` methode.\n    ``BaseWorker`` provide only a skeleton to help you to develop your own workers\n\n    .. note::\n        For conveniance, default recv method for backend socket is ``recv_string()`` from pyzmq.\n        But you can change it easily by overloading ``recv_func`` in your worker, for example::\n\n            def __init__(self, backend, *args, **kwargs):\n                super(MyWorkerClase, self).__init__(backend, *args, **kwargs)\n                self.recv_func = self.backend.recv_json()\n\n    :param str backend: backend zeromq string to connect to receiver. e.g: ``ipc://unix.socket``\n    '

    def __init__(self, backend, *args, **kwargs):
        self.context = zmq.Context()
        self.backend = self.context.socket(zmq.PULL)
        self.backend.connect(backend)
        self.recv_func = self.backend.recv_string

    def process_data(self, data):
        """Process data

        :param mixed data: data received from backend
        :raises: NotImplementedError
        """
        raise NotImplementedError('You must override the process data methode')

    def run(self):
        """Main loop for receive messages and process them

        ``self.recv_func`` is used to receive data from backend
        """
        try:
            while True:
                data = self.recv_func()
                self.process_data(data)

        except (Exception, KeyboardInterrupt) as e:
            log.error('Exception raised : %s', e)
            self.context.destroy()
            raise