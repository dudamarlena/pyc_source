# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dev\PyCharm Projects\NCryptoClient\NCryptoClient\Transmitter\client_sender.py
# Compiled at: 2018-04-19 18:23:41
# Size of source mod 2**32: 1871 bytes
"""
Module which defines Sender-thread class.
"""
import time
from threading import Thread
from queue import Queue
from NCryptoTools.Tools.utilities import send_msg, get_current_time
from NCryptoClient.client_instance_holder import client_holder

class Sender(Thread):
    __doc__ = '\n    Thread-class for controlling the flow of outgoing messages, storing them\n    into the buffer for outgoing messages.\n    '

    def __init__(self, shared_socket, wait_time=0.1, buffer_size=30):
        """
        Constructor. _output_buffer_queue is implemented as a queue.
        @param shared_socket: client socket.
        @param wait_time: wait time in seconds to avoid overheating.
        @param buffer_size: buffer size in number of elements.
        """
        super().__init__()
        self.daemon = True
        self._socket = shared_socket
        self._wait_time = wait_time
        self._output_buffer_queue = Queue(buffer_size)
        self._main_window = client_holder.get_instance('MainWindow')

    def add_msg_to_queue(self, jim_msg):
        """
        Stores new JSON-object in the outgoing queue.
        @param jim_msg: JSON-object (message).
        @return: -
        """
        self._output_buffer_queue.put(jim_msg)

    def run(self):
        """
        Runs thread routine.
        @return: -
        """
        while self._output_buffer_queue.qsize() > 0:
            jim_msg = self._output_buffer_queue.get()
            try:
                send_msg(self._socket, jim_msg)
            except OSError as e:
                self._main_window.add_data_in_tab('Log', '[{}] @NCryptoChat> {}'.format(get_current_time(), str(e)))

            time.sleep(self._wait_time)