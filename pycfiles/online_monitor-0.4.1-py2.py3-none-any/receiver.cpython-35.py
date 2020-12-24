# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/davidlp/git/online_monitor/online_monitor/receiver/receiver.py
# Compiled at: 2018-07-05 04:39:41
# Size of source mod 2**32: 5806 bytes
from pyqtgraph.Qt import QtCore
import zmq, logging
from threading import Event
from online_monitor.utils import utils

class DataWorker(QtCore.QObject):
    data = QtCore.pyqtSignal(dict)
    finished = QtCore.pyqtSignal()

    def __init__(self, deserializer):
        QtCore.QObject.__init__(self)
        self.deserializer = deserializer
        self._stop_readout = Event()
        self._send_data = None

    def connect_zmq(self, frontend_address, socket_type):
        self.context = zmq.Context()
        self.receiver = self.context.socket(socket_type)
        self.socket_type = socket_type
        if self.socket_type == zmq.SUB:
            self.receiver.setsockopt_string(zmq.SUBSCRIBE, '')
        self.receiver.set_hwm(10)
        self.receiver.connect(frontend_address)

    def receive_data(self):
        """ Infinite loop via QObject.moveToThread(), does not block event loop
        """
        while not self._stop_readout.wait(0.01):
            if self._send_data:
                if self.socket_type != zmq.DEALER:
                    raise RuntimeError('You send data without a bidirectional connection! Define a bidirectional connection.')
                self.receiver.send(self._send_data)
                self._send_data = None
            try:
                data_serialized = self.receiver.recv(flags=zmq.NOBLOCK)
                data = self.deserializer(data_serialized)
                self.data.emit(data)
            except zmq.Again:
                pass

        self.finished.emit()

    def shutdown(self):
        self._stop_readout.set()

    def send_data(self, data):
        self._send_data = data


class Receiver(QtCore.QObject):
    __doc__ = 'The receiver connects to a converter and vizualizes the data according\n    to the specified data type.\n\n    Usage:\n    '

    def __init__(self, frontend, kind, name='Undefined', loglevel='INFO', **kwarg):
        QtCore.QObject.__init__(self)
        self.kind = kind
        self.frontend_address = frontend
        self.name = name
        self.config = kwarg
        self._active = False
        self.socket_type = zmq.SUB
        self.frontend_address = self.frontend_address
        utils.setup_logging(loglevel)
        logging.debug('Initialize %s receiver %s at %s', self.kind, self.name, self.frontend_address)
        self.setup_receiver_device()
        self.setup_receiver()

    def set_bidirectional_communication(self):
        self.socket_type = zmq.DEALER

    def setup_receiver_device(self):
        logging.info('Start %s receiver %s at %s', self.kind, self.name, self.frontend_address)
        self.thread = QtCore.QThread()
        self.worker = DataWorker(self.deserialize_data)
        self.worker.moveToThread(self.thread)

    def active(self, value):
        self._active = value

    def start(self):
        self.worker.connect_zmq(self.frontend_address, self.socket_type)
        self.worker.finished.connect(self.thread.quit)
        self.worker.data.connect(self.handle_data_if_active)
        self.thread.started.connect(self.worker.receive_data)
        self.thread.finished.connect(self.finished_info)
        self.thread.start()

    def shutdown(self):
        self.worker.shutdown()
        self.thread.exit()
        self.thread.wait(500)

    def finished_info(self):
        logging.info('Close %s receiver %s at %s', self.kind, self.name, self.frontend_address)

    def handle_data_if_active(self, data):
        """ Forwards data to data handling function if reveiver is active"""
        if self._active:
            self.handle_data(data)

    def setup_receiver(self):
        """ Method can be defined to setup receiver specific parameters
            (e.g. bidirectional communication)
        """
        pass

    def setup_widgets(self, parent, name):
        raise NotImplementedError('You have to implement a setup_widgets method!')

    def handle_data(self, data):
        """ Handle data

            Receives a dictionary with data and sets the visualization
            accordningly. It is only called if the receiver is active.
        """
        raise NotImplementedError('You have to implement a handle_data method!')

    def send_command(self, command):
        self.worker.send_data(command)

    def deserialize_data(self, data):
        """ Has to convert the data do a python dict """
        raise NotImplementedError('You have to implement a deserialize_data method. Look at the examples!')