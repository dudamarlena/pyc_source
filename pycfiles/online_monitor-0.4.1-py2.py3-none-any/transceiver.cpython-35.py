# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/davidlp/git/online_monitor/online_monitor/converter/transceiver.py
# Compiled at: 2019-06-25 09:08:56
# Size of source mod 2**32: 11479 bytes
import multiprocessing, threading, zmq, logging, signal, psutil, sys
try:
    import queue
except ImportError:
    import Queue as queue

from online_monitor.utils import utils

class Transceiver(multiprocessing.Process):
    __doc__ = 'Every converter is a transceiver.\n\n    The transceiver connects a data source / multiple data sources\n    (e.g. DAQ systems, other converter, ...) and interprets the data according\n    to the specified data type. The interpreted data is published as a ZeroMQ\n    publisher.\n\n    Usage:\n    To specify a converter for a certain data type, inherit from this base\n    class and define these methods accordingly:\n        - setup_interpretation()\n        - deserialize_data()\n        - interpret_data()\n        - serialize_data()\n\n    New methods/objects that are not called/created within these function will\n    not work! Since a new process is created that only knows the objects\n    (and functions) defined there.\n\n    Parameter\n    ----------\n    backend_address : str, list\n        Address or list of adresses of the publishing device(s)\n    frontend_address : str\n        Address where the converter publishes the converted data\n    kind : str\n        String describing the kind of converter (e.g. forwarder)\n    max_buffer : number\n        Maximum messages buffered for interpretation, if exeeded\n        data is discarded. If None no limit is applied.\n    loglevel : str\n        The verbosity level for the logging (e.g. INFO, WARNING)\n    '

    def __init__(self, frontend, backend, kind, name='Undefined', max_buffer=None, loglevel='INFO', **kwarg):
        multiprocessing.Process.__init__(self)
        self.kind = kind
        self.frontend_address = frontend
        self.backend_address = backend
        self.max_buffer = max_buffer
        self.name = name
        self.frontend_socket_type = zmq.SUB
        self.backend_socket_type = zmq.PUB
        if 'max_cpu_load' in kwarg:
            logging.warning('The parameter max_cpu_load is deprecated! Use max_buffer!')
        self.config = kwarg
        if not isinstance(self.frontend_address, list):
            self.frontend_address = [
             self.frontend_address]
            self.n_frontends = 1
        else:
            self.n_frontends = len(self.frontend_address)
        if not isinstance(self.backend_address, list):
            self.backend_address = [
             self.backend_address]
            self.n_backends = 1
        else:
            self.n_backends = len(self.backend_address)
        self.exit = multiprocessing.Event()
        self.loglevel = loglevel
        utils.setup_logging(self.loglevel)
        self.setup_transceiver()
        logging.debug('Initialize %s converter %s with frontends %s and backends %s', self.kind, self.name, self.frontend_address, self.backend_address)

    def set_bidirectional_communication(self):
        logging.info('Set bidirectional communication for converter %s backend', self.name)
        self.backend_socket_type = zmq.DEALER

    def _setup_frontend(self):
        """ Receiver sockets facing clients (DAQ systems)
        """
        self.frontends = []
        self.fe_poller = zmq.Poller()
        for actual_frontend_address in self.frontend_address:
            actual_frontend = (actual_frontend_address,
             self.context.socket(self.frontend_socket_type))
            actual_frontend[1].setsockopt(zmq.LINGER, 500)
            actual_frontend[1].set_hwm(10)
            if self.frontend_socket_type == zmq.SUB:
                actual_frontend[1].setsockopt_string(zmq.SUBSCRIBE, '')
            actual_frontend[1].connect(actual_frontend_address)
            self.frontends.append(actual_frontend)
            self.fe_poller.register(actual_frontend[1], zmq.POLLIN)

        self.raw_data = queue.Queue()
        self.fe_stop = threading.Event()

    def _setup_backend(self):
        """ Send sockets facing services (e.g. online monitor, other forwarders)
        """
        self.backends = []
        self.be_poller = zmq.Poller()
        for actual_backend_address in self.backend_address:
            actual_backend = (actual_backend_address,
             self.context.socket(self.backend_socket_type))
            actual_backend[1].setsockopt(zmq.LINGER, 500)
            actual_backend[1].set_hwm(10)
            actual_backend[1].bind(actual_backend_address)
            self.backends.append(actual_backend)
            if self.backend_socket_type != zmq.DEALER:
                self.be_poller.register(actual_backend[1], zmq.POLLIN)

        self.be_stop = threading.Event()

    def _setup_transceiver(self):
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        self.context = zmq.Context()
        self._setup_frontend()
        self._setup_backend()

    def recv_data(self):
        while not self.fe_stop.is_set():
            self.fe_poller.poll(1)
            raw_data = []
            for actual_frontend in self.frontends:
                try:
                    actual_raw_data = actual_frontend[1].recv(flags=zmq.NOBLOCK)
                    if sys.version_info >= (3, 0):
                        actual_raw_data = actual_raw_data.decode('utf-8')
                    raw_data.append((actual_frontend[0],
                     self.deserialize_data(actual_raw_data)))
                except zmq.Again:
                    pass

            if raw_data:
                self.raw_data.put_nowait(raw_data)

    def recv_commands(self):
        if self.backend_socket_type == zmq.DEALER:
            while not self.be_stop.wait(0.1):
                self.be_poller.poll(1)
                commands = []
                if self.backend_socket_type == zmq.DEALER:
                    for actual_backend in self.backends:
                        try:
                            command = actual_backend[1].recv(zmq.NOBLOCK)
                            logging.debug('%s converter %s received command %s', self.kind, self.name, command)
                            commands.append(command)
                        except zmq.error.Again:
                            pass

                if commands:
                    self.handle_command(commands)

    def send_data(self, data):
        """ This function can be overwritten in derived class

            Std. function is to broadcast all receiver data to all backends
        """
        for frontend_data in data:
            serialized_data = self.serialize_data(frontend_data)
            if sys.version_info >= (3, 0):
                serialized_data = serialized_data.encode('utf-8')
            for actual_backend in self.backends:
                actual_backend[1].send(serialized_data)

    def run(self):
        utils.setup_logging(self.loglevel)
        self._setup_transceiver()
        self.setup_interpretation()
        process = psutil.Process(self.ident)
        self.cpu_load = 0.0
        be_thread = threading.Thread(target=self.recv_commands)
        be_thread.start()
        fe_thread = threading.Thread(target=self.recv_data)
        fe_thread.start()
        logging.debug('Start %s transceiver %s at %s', self.kind, self.name, self.backend_address)
        while not self.exit.wait(0.01):
            if self.raw_data.empty():
                continue
            else:
                raw_data = self.raw_data.get_nowait()
            actual_cpu_load = process.cpu_percent()
            self.cpu_load = 0.9 * self.cpu_load + 0.1 * actual_cpu_load
            if not self.max_buffer or self.max_buffer > self.raw_data.qsize():
                data = self.interpret_data(raw_data)
                if data is not None and len(data) != 0:
                    self.send_data(data)
                else:
                    logging.warning('Converter cannot keep up, omitting data for interpretation!')

        self.be_stop.set()
        be_thread.join()
        self.fe_stop.set()
        fe_thread.join()
        for actual_frontend in self.frontends:
            actual_frontend[1].close()

        for actual_backend in self.backends:
            actual_backend[1].close()

        self.context.term()
        logging.debug('Close %s transceiver %s at %s', self.kind, self.name, self.backend_address)

    def shutdown(self):
        self.exit.set()

    def setup_transceiver(self):
        """ Method can be defined to setup transceiver specific parameters

            (e.g. bidirectional communication)
        """
        pass

    def setup_interpretation(self):
        pass

    def deserialize_data(self, data):
        return data

    def interpret_data(self, data):
        raise NotImplementedError('You have to implement a interpret_data method!')

    def serialize_data(self, data):
        return data

    def handle_command(self, commands):
        """ Command received from a receiver (bidir. commun. mode)."""
        raise NotImplementedError('You have to implement a handle_command method!')